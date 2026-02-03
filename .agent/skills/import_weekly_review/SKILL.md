---
name: import_weekly_review
description: Notionからエクスポートされた最新のWeekly Review (CSV) を自動検出し、今週分のデータをMarkdownに変換してweeklyフォルダに保存・整理します。
version: 1.0.0
---

# Import Weekly Review

このスキルは、Notionからエクスポートされた「Weekly Review」CSVファイルを処理し、Markdown形式のレビューファイルを作成します。

## 処理の流れ

1. `/Users/310tea/Documents/学習アウトプット/notion_exports` フォルダ内の最新の `Weekly Review*.csv` を検索します。
2. CSV内から「今週（実行日を含む週）」のデータを抽出します。見つからない場合は最新の週を使用します。
3. データをMarkdown形式に整形し、以下の命名規則で保存します。
   - `/Users/310tea/Documents/学習アウトプット/weekly/weekly_YYYY-MM-DD_to_YYYY-MM-DD.md`
4. 元のCSVファイルを削除します。

## 使用方法

NotionからCSVをエクスポートした後、このスキルを実行してください。

```bash
python3 /Users/310tea/Documents/学習アウトプット/.agent/skills/import_weekly_review/scripts/process_weekly_export.py
```
