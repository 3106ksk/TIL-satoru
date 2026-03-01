---
name: generate-runteq-report
description: This skill generates Runteq daily report from detailed learning logs (daily/daily_YYYY-MM-DD.md files). Use this skill when the user requests to create a daily report, Runteq report, or daily journal. Trigger phrases include "日誌を作成して", "Runteq日誌を作成して", "daily reportを生成して".
---

# Generate Runteq Report

## Overview

Generate concise Runteq daily reports from detailed learning logs. Extract key sections (Stats, Top1/Done条件, learning records, technical learnings) and format them for Runteq submission.

## Usage

When the user requests a daily report, use the provided Python script to generate it:

```bash
python3 scripts/generate_runteq_report.py <date>
```

**Example:**
```bash
python3 scripts/generate_runteq_report.py 2026-02-19
```

**Input:** `daily/daily_YYYY-MM-DD.md` (detailed learning log)
**Output:** `daily_reports/daily_report_YYYY-MM-DD.md` (Runteq submission format)

## Report Format

The generated report includes:

1. **Stats** - Learning tasks breakdown with time (without DS scores or details)
2. **Top1 / Done条件 / 切れたら** - Daily plan (without feedback)
3. **1日の感想** - Empty section for manual input
4. **今日の学習記録** - Learning record (as-is from source)
5. **Technical Learnings** - Technical learnings (as-is from source)

## Script

Use `scripts/generate_runteq_report.py` to automate the conversion. The script:

- Extracts learning tasks and times from the feedback section
- Removes DS scores and detailed breakdowns
- Formats task names in bold
- Creates the "1日の感想" placeholder section
- Copies learning records and technical learnings as-is
