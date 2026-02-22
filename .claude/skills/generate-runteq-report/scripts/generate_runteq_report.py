#!/usr/bin/env python3
"""
Generate Runteq daily report from daily log file.

Usage:
    python3 generate_runteq_report.py <date>
    python3 generate_runteq_report.py 2026-02-19
"""

import re
import sys
from pathlib import Path


def extract_section(content: str, section_title: str) -> str:
    """Extract a section from markdown content by title."""
    pattern = rf'^## ■ {re.escape(section_title)}\n(.*?)(?=^## ■ |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_tasks_from_feedback(content: str) -> list[str]:
    """Extract task list with time from feedback section."""
    feedback_section = extract_section(content, 'Top1 / Done条件 達成度フィードバック')
    if not feedback_section:
        return []

    tasks = []
    task_dict = {}  # Use dict to avoid duplicates

    # Pattern 1: "DeviseリサーチはSessionsで31 min"
    matches = re.findall(r'(\w+リサーチ).*?(\d+)\s*min', feedback_section)
    for task_name, time in matches:
        task_dict[task_name] = time

    # Pattern 2: "エンティティ・テーブル・ER図の設計は64+36+72+27=199 min"
    matches = re.findall(r'(エンティティ[^は]+設計)は.*?=\s*(\d+)\s*min', feedback_section)
    for task_name, time in matches:
        # Normalize task name
        task_name = task_name.replace('の設計', '設計')
        task_dict[task_name] = time

    # Pattern 3: "rails new + GitHub pushは...= 167 min"
    matches = re.findall(r'(rails\s+new\s*\+\s*GitHub\s+push).*?=\s*(\d+)\s*min', feedback_section)
    for task_name, time in matches:
        task_dict[task_name] = time

    # Pattern 4: "mini_app_dev (74分) + Other (12分)"
    matches = re.findall(r'(\w+)\s*\((\d+)分\)', feedback_section)
    for task_name, time in matches:
        task_dict[task_name] = time

    # Convert dict to list
    for task_name, time in task_dict.items():
        tasks.append(f'- **{task_name}**: {time} min')

    return tasks


def extract_top1_section(content: str) -> dict:
    """Extract Top1, Done条件, and 切れたら from content."""
    section = extract_section(content, 'Stats')

    result = {}
    for line in section.split('\n'):
        if line.startswith('- **Top1**:'):
            result['top1'] = line.replace('- **Top1**:', '').strip()
        elif line.startswith('- **Done条件**:'):
            result['done'] = line.replace('- **Done条件**:', '').strip()
        elif line.startswith('- **切れたら→**:'):
            result['kireTara'] = line.replace('- **切れたら→**:', '').strip()

    return result


def generate_runteq_report(daily_file_path: Path, output_file_path: Path):
    """Generate Runteq daily report from daily log file."""

    # Read input file
    if not daily_file_path.exists():
        print(f"Error: Input file not found: {daily_file_path}")
        sys.exit(1)

    content = daily_file_path.read_text(encoding='utf-8')

    # Extract sections
    tasks = extract_tasks_from_feedback(content)
    top1_data = extract_top1_section(content)
    learning_record = extract_section(content, '今日の学習記録')
    technical_learnings = extract_section(content, 'Technical Learnings')

    # Extract date from filename
    date_match = re.search(r'daily_(\d{4}-\d{2}-\d{2})\.md', daily_file_path.name)
    date = date_match.group(1) if date_match else 'YYYY-MM-DD'

    # Build output content
    output_lines = [
        f'# Runteq日誌レポート - {date}',
        '',
        '## ■ Stats',
        '',
        '1日の学習タスクの内訳と時間',
    ]

    output_lines.extend(tasks)
    output_lines.extend([
        '',
        '---',
        '',
        '## ■ Top1 / Done条件 / 切れたら',
        '',
        f'- **Top1**: {top1_data.get("top1", "")}',
        f'- **Done条件**: {top1_data.get("done", "")}',
        f'- **切れたら→**: {top1_data.get("kireTara", "")}',
        '',
        '---',
        '',
        '## ■ 1日の感想',
        '',
        '（ここに手書きで感想を記入）',
        '',
        '---',
        '',
        f'## ■ 今日の学習記録',
        '',
        learning_record,
        '',
        '---',
        '',
        f'## ■ Technical Learnings',
        '',
        technical_learnings,
    ])

    # Write output file
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    output_file_path.write_text('\n'.join(output_lines), encoding='utf-8')

    print(f'✅ Generated: {output_file_path}')


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_runteq_report.py <date>")
        print("Example: python3 generate_runteq_report.py 2026-02-19")
        sys.exit(1)

    date = sys.argv[1]

    # Validate date format
    if not re.match(r'\d{4}-\d{2}-\d{2}', date):
        print(f"Error: Invalid date format '{date}'. Expected YYYY-MM-DD")
        sys.exit(1)

    # Determine project root (assuming script is in .claude/skills/*/scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent.parent

    daily_file = project_root / 'daily' / f'daily_{date}.md'
    output_file = project_root / 'daily_reports' / f'daily_report_{date}.md'

    generate_runteq_report(daily_file, output_file)


if __name__ == '__main__':
    main()
