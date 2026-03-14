---
name: extract_daily_sessions
description: Sessions CSVから指定日のセッションレコードを抽出し、サマリーメトリクス付きの構造化Markdownを生成する。
---

# Extract Daily Sessions Skill

Notion Sessions DB CSVから指定した1日分のセッションレコードを抽出し、サマリーメトリクス・セッション一覧・Notes詳細を含む構造化Markdownを生成する。出力は `format_daily_log` スキルの参照データとしても活用可能。

## Usage

1. **入力CSVを特定**: `notion_exports/ExportBlock-.../Sessions/Sessions DB*.csv` を確認
2. **対象日付を決定**: 抽出したい日付（YYYY-MM-DD）
3. **スクリプトを実行**

## Instructions for Agent

1. **入力ファイルの確認**:
    - `notion_exports/` 配下のSessions DB CSVファイルパスを特定する
    - ファイルの存在を確認する

2. **スクリプト実行**:
    ```bash
    python3 /Users/310tea/Documents/Learning_log/.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py \
      "<input_csv_path>" \
      "YYYY-MM-DD" \
      "/Users/310tea/Documents/Learning_log/daily_sessions_record"
    ```

3. **出力確認**:
    - `daily_sessions_record/sessions_YYYY-MM-DD.md` が生成されたことを確認する
    - 結果をユーザーに報告する

4. **クリーンアップ**:
    - 元のCSVファイルが他のスキル（`process_sessions_db_export`等）でも使用される場合は削除しない
    - CSVが不要であることをユーザーに確認してから削除する

## Output Format

```markdown
# Sessions Record: YYYY-MM-DD (Week YYYY-W##)

## Summary
| Metric | Value |
|--------|-------|
| Total Sessions | N |
| Total Duration | Xmin (Xh Xm) |
| Deep Flag Sessions | X / N |
| Avg Deep Score (active) | X.X |

## Sessions
| # | Start | End | Duration | Type | Deep Score | Deep Flag | CH | Focus | Friction |
(rows)

## Notes
### #1 type (start–end)
- **やった**: ...
- **詰まった/気づいた**: ...
```

## Integration with format_daily_log

`format_daily_log` スキルがdaily reviewを生成する際、生CSVを直接パースする代わりに `daily_sessions_record/sessions_YYYY-MM-DD.md` を参照データとして利用できる。事前に本スキルで抽出しておくことで、セッションデータの構造化が済んだ状態で日次レビュー整形に集中できる。

## Prerequisites

- Python 3

## Example

**ユーザー指示**: 「3/3のセッション記録を抽出して」

**実行**:
```bash
python3 /Users/310tea/Documents/Learning_log/.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py \
  "/Users/310tea/Documents/Learning_log/notion_exports/ExportBlock-.../Sessions/Sessions DB*.csv" \
  "2026-03-03" \
  "/Users/310tea/Documents/Learning_log/daily_sessions_record"
```
