---
name: normalize_learning_log
description: Notionエクスポート（Sessions CSV + Daily Review MD）を読み込み、週次分析用の正規化JSONデータを自動生成する。
---

# Normalize Learning Log

`notion_exports` のSessionログ(CSV)と `daily/` のMarkdownファイルを結合・正規化し、分析用JSONファイルを生成する。

## 処理内容

1. **入力データの検索**:
   - `notion_exports/ExportBlock-*/Sessions/Sessions DB*.csv`（最新のもの）
   - `daily/daily_YYYY-MM-DD.md`（CSVの日付に対応するもの）

2. **正規化処理**:
   - 日時形式の統一 (ISO 8601)
   - カテゴリのマッピング (Coding, Reading, Interview, Planning, Other)
   - Daily Review (`Worked`, `Slipped`, `Insight`, `Strategy for Next Day`) の結合
   - `Day Mode` (Shift/Off) の判定

3. **出力**:
   - (AI分析用) `normalized_data/normalized_data_{start}_to_{end}.json`
   - (保管用) `Sessions/Sessions_DB_{start}_to_{end}.md`

## 使用方法

Notionからデータをエクスポートした後、以下のコマンドを実行するか「学習ログを正規化して」と指示。

```bash
python3 .claude/normalize_learning_log/scripts/normalize.py
```

## スクリプト

- `scripts/normalize.py`: CSV + MD → JSON 正規化スクリプト

## 参照

- `.claude/format_daily_log/SKILL.md`: daily MDの入力フォーマット定義
- `prompts/analysis_prompt_v2.md`: 出力JSONを入力とする週次分析プロンプト
