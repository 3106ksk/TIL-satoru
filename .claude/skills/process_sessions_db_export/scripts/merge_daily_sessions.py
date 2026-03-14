#!/usr/bin/env python3
"""
daily_sessions_record/ の1日毎セッションファイルを結合し、
Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md を生成する。

Usage:
    python3 merge_daily_sessions.py <start_date> <end_date>
    python3 merge_daily_sessions.py 2026-03-02 2026-03-08
"""

import os
import re
import sys
from datetime import datetime, timedelta

BASE_DIR = '/Users/310tea/Documents/Learning_log'
INPUT_DIR = os.path.join(BASE_DIR, 'daily_sessions_record')
OUTPUT_DIR = os.path.join(BASE_DIR, 'Sessions')

# Sessions_DB_*.md のヘッダー（normalize.py が参照するカラムを含む）
HEADERS = [
    ' learning content', 'Cognitive Headroom', 'Daily Review', 'Date',
    'Deep Flag', 'Deep Score', 'Deep Work Min', 'Focus', 'Friction',
    'In Last Week', 'In This Week', 'Interview Min', 'Notes', 'Prep Min',
    'Status', 'TI Min', 'Type', 'WeekKey', 'WrapUp Min', 'duration (m)f',
    'end time', 'start time', '作成日時'
]


def parse_time_to_datetime(date_str, time_str):
    """'7:29' + '2026-03-03' -> 'March 3, 2026 7:29 AM (GMT+9)'"""
    if not time_str or time_str == '-':
        return ''
    try:
        h, m = map(int, time_str.strip().split(':'))
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        dt = dt.replace(hour=h, minute=m)
        suffix = 'AM' if h < 12 else 'PM'
        display_h = h if h <= 12 else h - 12
        if display_h == 0:
            display_h = 12
        return dt.strftime(f'%B {dt.day}, %Y {display_h}:%M {suffix} (GMT+9)')
    except (ValueError, AttributeError):
        return ''


def parse_duration(dur_str):
    """'44m' -> '44', '1h 27m' -> '87'"""
    if not dur_str or dur_str == '-':
        return '0'
    total = 0
    h_match = re.search(r'(\d+)h', dur_str)
    m_match = re.search(r'(\d+)m', dur_str)
    if h_match:
        total += int(h_match.group(1)) * 60
    if m_match:
        total += int(m_match.group(1))
    return str(total) if total > 0 else '0'


def get_week_key(date_str):
    """'2026-03-03' -> '2026-W10'"""
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    return f"{dt.isocalendar()[0]}-W{dt.isocalendar()[1]:02d}"


def parse_session_file(file_path, date_str):
    """1日分のセッションファイルをパースし、行データのリストを返す"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    sessions = []
    notes_map = {}  # session_num -> notes text

    # --- Sessions テーブルをパース ---
    in_table = False
    header_found = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('| #') and 'Start' in stripped:
            in_table = True
            header_found = False
            continue
        if in_table and stripped.startswith('|---'):
            header_found = True
            continue
        if in_table and header_found and stripped.startswith('|'):
            cols = [c.strip() for c in stripped.split('|')[1:-1]]
            if len(cols) >= 10:
                sessions.append({
                    'num': cols[0],
                    'start': cols[1],
                    'end': cols[2],
                    'duration': cols[3],
                    'type': cols[4],
                    'deep_score': cols[5],
                    'deep_flag': cols[6],
                    'ch': cols[7],
                    'focus': cols[8],
                    'friction': cols[9],
                })
        elif in_table and header_found and not stripped.startswith('|'):
            in_table = False

    # --- Notes セクションをパース ---
    note_pattern = re.compile(r'^### #(\d+)\s+')
    current_note_num = None
    current_note_lines = []

    for line in lines:
        stripped = line.strip()
        match = note_pattern.match(stripped)
        if match:
            if current_note_num is not None:
                notes_map[current_note_num] = '<br>'.join(current_note_lines)
            current_note_num = match.group(1)
            current_note_lines = []
            continue
        if current_note_num is not None:
            if stripped.startswith('- **'):
                current_note_lines.append(stripped.lstrip('- '))
            elif stripped and not stripped.startswith('#'):
                current_note_lines.append(stripped)

    if current_note_num is not None:
        notes_map[current_note_num] = '<br>'.join(current_note_lines)

    # --- Sessions_DB 行に変換 ---
    week_key = get_week_key(date_str)
    rows = []
    for s in sessions:
        deep_score = s['deep_score']
        try:
            ds_val = float(deep_score)
        except ValueError:
            ds_val = 0

        deep_flag = s['deep_flag']
        dur = parse_duration(s['duration'])

        # Deep Work Min: Deep Flag が Yes の場合のみ duration を記録
        deep_work_min = dur if deep_flag == 'Yes' else '0'

        start_dt = parse_time_to_datetime(date_str, s['start'])
        end_dt = parse_time_to_datetime(date_str, s['end'])

        notes_text = notes_map.get(s['num'], '')

        ch = s['ch'] if s['ch'] != '-' else ''
        focus = s['focus'] if s['focus'] != '-' else ''
        friction = s['friction'] if s['friction'] != '-' else ''

        row = {
            ' learning content': '',
            'Cognitive Headroom': ch,
            'Daily Review': '',
            'Date': date_str,
            'Deep Flag': deep_flag,
            'Deep Score': deep_score,
            'Deep Work Min': deep_work_min,
            'Focus': focus,
            'Friction': friction,
            'In Last Week': 'No',
            'In This Week': 'Yes',
            'Interview Min': '0',
            'Notes': notes_text,
            'Prep Min': '0',
            'Status': 'Done',
            'TI Min': '',
            'Type': s['type'],
            'WeekKey': week_key,
            'WrapUp Min': '0',
            'duration (m)f': dur,
            'end time': end_dt,
            'start time': start_dt,
            '作成日時': start_dt.replace(' (GMT+9)', '') if start_dt else '',
        }
        rows.append(row)

    return rows


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <start_date> <end_date>")
        print(f"Example: {sys.argv[0]} 2026-03-02 2026-03-08")
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("Error: Date format must be YYYY-MM-DD")
        sys.exit(1)

    # 範囲内の日付を列挙
    all_rows = []
    current = start_dt
    found_files = []
    while current <= end_dt:
        date_str = current.strftime('%Y-%m-%d')
        file_path = os.path.join(INPUT_DIR, f'sessions_{date_str}.md')
        if os.path.exists(file_path):
            found_files.append(date_str)
            rows = parse_session_file(file_path, date_str)
            all_rows.extend(rows)
            print(f"  Parsed: {date_str} ({len(rows)} sessions)")
        else:
            print(f"  Skipped: {date_str} (no file)")
        current += timedelta(days=1)

    if not all_rows:
        print("Error: No session data found in the specified date range.")
        sys.exit(1)

    print(f"\nTotal: {len(all_rows)} sessions from {len(found_files)} days")

    # Markdown テーブル生成
    header_line = '| ' + ' | '.join(HEADERS) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(HEADERS)) + ' |'

    table_lines = [header_line, separator]
    for row in all_rows:
        values = [str(row.get(h, '')) for h in HEADERS]
        table_lines.append('| ' + ' | '.join(values) + ' |')

    # 出力
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = f"Sessions_DB_{start_date}_to_{end_date}.md"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(table_lines) + '\n')

    print(f"\nSuccess! Output: {output_path}")


if __name__ == '__main__':
    main()
