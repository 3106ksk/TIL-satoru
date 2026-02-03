---
name: normalize_learning_log
description: Notionからエクスポートされた学習ログ(Sessions CSV)とDaily Review(Markdown)を読み込み、定性分析用に正規化されたJSONデータを自動生成します。
version: 1.0.0
---

# Normalize Learning Log

このスキルは、`notion_exports` フォルダにある最新のSessionログ(CSV)と、`daily` フォルダにあるMarkdownファイルを結合・正規化し、分析用JSONファイルを生成します。

## 処理内容

1. **入力データの検索**:
   - `/Users/310tea/Documents/学習アウトプット/notion_exports/Sessions DB*.csv` (最新のもの)
   - `/Users/310tea/Documents/学習アウトプット/daily/daily_YYYY-MM-DD.md` (CSVの日付に対応するもの)

2. **正規化処理**:
   - 日時形式の統一 (ISO 8601)
   - カテゴリのマッピング (Coding, Reading, Interview, Planning, Other)
   - Daily Review (`Worked`, `Slipped`, `Insight`) の結合
   - `Day Mode` (Shift/Off) の判定

3. **出力**:
   - (AI分析用) `/Users/310tea/Documents/学習アウトプット/normalized_data/normalized_data_{start}_to_{end}.json`
   - (保管用) `/Users/310tea/Documents/学習アウトプット/Sessions/Sessions_DB_{start}_to_{end}.md`

これで、以前のスキル (`process_sessions_db_export`) の機能もこのスキルに含まれるため、一回の実行で「分析用データ作成」と「ログ保管」の両方が完了します。

## 使用方法

Notionからデータをエクスポートした後、以下のコマンドを実行するか、チャットで「学習ログを正規化して」と指示してください。

```bash
python3 /Users/310tea/Documents/学習アウトプット/.agent/skills/normalize_learning_log/scripts/normalize.py
```
