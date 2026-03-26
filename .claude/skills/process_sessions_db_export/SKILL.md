---
name: process_sessions_db_export
description: daily_sessions_record の日次セッションファイルを結合し、normalize.py 互換の Sessions_DB Markdown を生成する。
---

# Process Sessions DB Export Skill

`daily_sessions_record/sessions_YYYY-MM-DD.md` を指定日付範囲で結合し、`Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md` を生成する。生成されたファイルは `normalize_learning_log` スキルの入力として使用される。

## Usage

```bash
python3 /Users/310tea/Documents/Learning_log/.claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py <start_date> <end_date>
```

- **入力**: `daily_sessions_record/sessions_YYYY-MM-DD.md`（日付範囲内のファイル）
- **出力**: `Sessions/Sessions_DB_<start_date>_to_<end_date>.md`

## Instructions for Agent

1. **日付範囲の決定**: ユーザーの指示から開始日・終了日（YYYY-MM-DD）を特定する。
2. **スクリプト実行**:
    ```bash
    python3 /Users/310tea/Documents/Learning_log/.claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py \
      "YYYY-MM-DD" \
      "YYYY-MM-DD"
    ```
3. **出力確認**: `Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md` が生成されたことを確認し、セッション数をユーザーに報告する。

## 変換処理の内容

- 短縮時刻 ("7:29") → Notion形式 ("March 3, 2026 7:29 AM (GMT+9)")
- Duration ("44m", "1h 27m") → 整数分
- Notes `### #N` セクション → `<br>` 区切りインライン
- WeekKey 自動算出、全23カラム生成

## Example

**User Request**: 「今週のセッションを処理して（3/8〜3/14）」

**Action**:
```bash
python3 /Users/310tea/Documents/Learning_log/.claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py \
  "2026-03-08" \
  "2026-03-14"
```

## Prerequisites

- Python 3
- `daily_sessions_record/` に対象日付のセッションファイルが存在すること

## スクリプト

- `scripts/merge_daily_sessions.py`: daily_sessions_record → Sessions_DB 変換スクリプト

## 参照

- `.claude/skills/normalize_learning_log/SKILL.md`: 生成された Sessions_DB を入力とする正規化スキル
- `.claude/skills/extract_daily_sessions/SKILL.md`: daily_sessions_record ファイルを生成するスキル
