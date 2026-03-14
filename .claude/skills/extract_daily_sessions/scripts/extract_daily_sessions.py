#!/usr/bin/env python3
"""Extract single-day session records from a Notion Sessions CSV and generate structured Markdown."""

import csv
import sys
import os
import re
import argparse
from datetime import datetime


# Required columns for extraction
REQUIRED_COLUMNS = [
    'Date', 'duration (m)f', 'start time', 'end time',
    'Type', 'Notes', 'CH', 'Focus',
    'Friction', 'Deep Score', 'Deep Flag'
]

# Optional columns
OPTIONAL_COLUMNS = ['WeekKey']

# Session types excluded from active Deep Score average
INACTIVE_TYPES = {'rest', 'exercise'}


def detect_column_indices(header):
    """Detect column indices by name, handling BOM and whitespace."""
    cleaned = [col.strip().lstrip('\ufeff') for col in header]
    indices = {}

    # Required columns
    for col_name in REQUIRED_COLUMNS:
        for i, h in enumerate(cleaned):
            if h == col_name:
                indices[col_name] = i
                break
    missing = [c for c in REQUIRED_COLUMNS if c not in indices]
    if missing:
        print(f"Error: Missing required columns: {missing}")
        print(f"Available columns: {cleaned}")
        sys.exit(1)

    # Optional columns
    for col_name in OPTIONAL_COLUMNS:
        for i, h in enumerate(cleaned):
            if h == col_name:
                indices[col_name] = i
                break

    return indices


def parse_notion_timestamp(timestamp_str):
    """Parse Notion timestamp to short time string (e.g. '7:29').

    Input format: 'March 3, 2026 7:29 AM (GMT+9)'
    """
    if not timestamp_str or not timestamp_str.strip():
        return None, '-'
    clean = re.sub(r'\s*\(.*\)', '', timestamp_str).strip()
    try:
        dt = datetime.strptime(clean, '%B %d, %Y %I:%M %p')
        return dt, dt.strftime('%-H:%M')
    except ValueError:
        return None, '-'


def parse_notes(notes_str):
    """Parse Notes field into structured sections.

    Expected format:
        やった：<content>
        詰まった/気づいた：<content>
        次：<content>
    """
    if not notes_str or not notes_str.strip():
        return {}

    result = {}
    # Split by known prefixes
    patterns = [
        ('やった', r'やった[：:](.+?)(?=詰まった|気づいた|次[：:]|$)'),
        ('詰まった/気づいた', r'(?:詰まった/気づいた|詰まった|気づいた)[：:](.+?)(?=次[：:]|$)'),
    ]
    for key, pattern in patterns:
        match = re.search(pattern, notes_str, re.DOTALL)
        if match:
            value = match.group(1).strip()
            if value:
                result[key] = value
    return result


def is_type_inactive(type_str):
    """Check if session type is Rest or Exercise."""
    if not type_str:
        return False
    return type_str.strip().lower() in INACTIVE_TYPES


def safe_float(val, default=0.0):
    """Safely parse a float value."""
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val, default='-'):
    """Safely parse an int for display."""
    try:
        v = float(val)
        if v == int(v):
            return str(int(v))
        return str(v)
    except (ValueError, TypeError):
        return default


def calculate_week_key(date_str):
    """Calculate week key from date string (YYYY-MM-DD).

    Returns format: YYYY-W##
    """
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        iso_year, iso_week, _ = dt.isocalendar()
        return f"{iso_year}-W{iso_week:02d}"
    except ValueError:
        return 'unknown'


def compute_summary(rows, idx):
    """Compute summary metrics from filtered rows."""
    total_sessions = len(rows)
    total_duration = sum(safe_float(r[idx['duration (m)f']]) for r in rows)

    deep_flag_count = sum(1 for r in rows if r[idx['Deep Flag']].strip().lower() == 'yes')

    # Average Deep Score excluding Rest/Exercise
    active_scores = []
    for r in rows:
        if not is_type_inactive(r[idx['Type']]):
            score = safe_float(r[idx['Deep Score']], default=None)
            if score is not None:
                active_scores.append(score)

    avg_deep = sum(active_scores) / len(active_scores) if active_scores else 0.0

    hours = int(total_duration) // 60
    mins = int(total_duration) % 60

    return {
        'total_sessions': total_sessions,
        'total_duration': int(total_duration),
        'duration_formatted': f"{int(total_duration)} min ({hours}h {mins}m)",
        'deep_flag': f"{deep_flag_count} / {total_sessions}",
        'avg_deep_score': round(avg_deep, 1),
    }


def build_sessions_table(rows, idx):
    """Build the sessions table lines."""
    lines = []
    lines.append('| # | Start | End | Duration | Type | Deep Score | Deep Flag | CH | Focus | Friction |')
    lines.append('|---|-------|-----|----------|------|------------|-----------|-----|-------|----------|')

    for i, r in enumerate(rows, 1):
        _, start_short = parse_notion_timestamp(r[idx['start time']])
        _, end_short = parse_notion_timestamp(r[idx['end time']])
        duration = f"{int(safe_float(r[idx['duration (m)f']]))}m"
        session_type = r[idx['Type']].strip() if r[idx['Type']].strip() else '-'
        deep_score = safe_int(r[idx['Deep Score']])
        deep_flag = r[idx['Deep Flag']].strip() if r[idx['Deep Flag']].strip() else '-'
        ch = safe_int(r[idx['CH']])
        focus = safe_int(r[idx['Focus']])
        friction = safe_int(r[idx['Friction']])

        lines.append(f'| {i} | {start_short} | {end_short} | {duration} | {session_type} | {deep_score} | {deep_flag} | {ch} | {focus} | {friction} |')

    return lines


def build_notes_section(rows, idx):
    """Build the per-session notes section."""
    lines = []

    for i, r in enumerate(rows, 1):
        _, start_short = parse_notion_timestamp(r[idx['start time']])
        _, end_short = parse_notion_timestamp(r[idx['end time']])
        session_type = r[idx['Type']].strip() if r[idx['Type']].strip() else '-'

        notes = parse_notes(r[idx['Notes']])
        lines.append(f'### #{i} {session_type} ({start_short}\u2013{end_short})')

        if notes:
            for key in ['やった', '詰まった/気づいた']:
                if key in notes:
                    lines.append(f'- **{key}**: {notes[key]}')
        lines.append('')

    return lines


def generate_markdown(target_date, week_key, summary, sessions_table, notes_section):
    """Assemble the final markdown document."""
    lines = []
    lines.append(f'# Sessions Record: {target_date} (Week {week_key})')
    lines.append('')
    lines.append('## Summary')
    lines.append('')
    lines.append('| Metric | Value |')
    lines.append('|--------|-------|')
    lines.append(f'| Total Sessions | {summary["total_sessions"]} |')
    lines.append(f'| Total Duration | {summary["duration_formatted"]} |')
    lines.append(f'| Deep Flag Sessions | {summary["deep_flag"]} |')
    lines.append(f'| Avg Deep Score (active) | {summary["avg_deep_score"]} |')
    lines.append('')
    lines.append('## Sessions')
    lines.append('')
    lines.extend(sessions_table)
    lines.append('')
    lines.append('## Notes')
    lines.append('')
    lines.extend(notes_section)

    return '\n'.join(lines)


def extract_daily_sessions(input_path, target_date, output_dir):
    """Main extraction logic."""
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    # Read CSV
    print(f"Reading from: {input_path}")
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            print("Error: Empty CSV file")
            sys.exit(1)

        idx = detect_column_indices(header)
        all_rows = list(reader)

    # Filter by target date
    date_col = idx['Date']
    filtered = [r for r in all_rows if len(r) > date_col and r[date_col].strip() == target_date]

    print(f"Found {len(filtered)} sessions for {target_date}")

    # Sort by start time
    def sort_key(row):
        dt, _ = parse_notion_timestamp(row[idx['start time']])
        return dt or datetime.min

    filtered.sort(key=sort_key)

    # Output path
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"sessions_{target_date}.md"
    output_path = os.path.join(output_dir, output_filename)

    # Handle no records
    if not filtered:
        print(f"Warning: No sessions found for {target_date}")
        week_key = calculate_week_key(target_date)
        md = f"# Sessions Record: {target_date} (Week {week_key})\n\nNo sessions recorded for this date.\n"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        print(f"Created (empty): {output_path}")
        return output_path

    # Extract week key
    if 'WeekKey' in idx and filtered[0][idx['WeekKey']].strip():
        week_key = filtered[0][idx['WeekKey']].strip()
    else:
        week_key = calculate_week_key(target_date)

    # Build components
    summary = compute_summary(filtered, idx)
    sessions_table = build_sessions_table(filtered, idx)
    notes_section = build_notes_section(filtered, idx)

    # Generate and write
    markdown = generate_markdown(target_date, week_key, summary, sessions_table, notes_section)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    print(f"Successfully created: {output_path}")
    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract daily sessions from Notion Sessions CSV')
    parser.add_argument('input_csv', help='Path to the Sessions DB CSV file')
    parser.add_argument('target_date', help='Target date (YYYY-MM-DD)')
    parser.add_argument('output_dir', help='Output directory for the Markdown file')

    args = parser.parse_args()
    extract_daily_sessions(args.input_csv, args.target_date, args.output_dir)
