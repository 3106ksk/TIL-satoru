---
name: normalize_learning_log
description: Notionエクスポート（Sessions CSV + Daily Review MD）を読み込み、週次分析用の正規化JSONデータを自動生成する。
---

# Normalize Learning Log

`notion_exports` のSessionログ(CSV)と `daily/` のMarkdownファイルを結合・正規化し、分析用JSONファイルを生成する。

## 処理内容

1. **入力データの検索**:
   - `Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md`（`process_sessions_db_export` スキル実行後に生成されるもの）
   - `daily/daily_YYYY-MM-DD.md`（対象週に対応するもの）

2. **正規化処理**:
   - 日時形式の統一 (ISO 8601)
   - カテゴリのマッピング (Coding, Reading, Interview, Planning, Other)
   - Daily Review (`Worked`, `Slipped`, `Insight`, `Strategy for Next Day`) の結合
   - `Day Mode` (Shift/Off) の判定

3. **出力**:
   - (AI分析用) `normalized_data/normalized_data_{start}_to_{end}.json`

## 使用方法

**AIエージェントへの指示**:
「1週間のログを正規化して」や「学習ログを正規化して」と指示された場合、本スキルが単独で動く前に**必ず以下の2ステップを順に実行してください**。

1. **`process_sessions_db_export` スキルの実行**: 最新の Notion CSV エクスポートから `Sessions_DB_*.md` を生成する。
2. **本スキルの実行**: 生成された Markdown ファイルを入力として以下のコマンドを実行し、JSONを生成する。

```bash
python3 .agent/skills/normalize_learning_log/scripts/normalize.py
```

## スクリプト

- `scripts/normalize.py`: Sessions MD + daily MD → JSON 正規化スクリプト

## 参照

- `.agent/skills/format_daily_log/SKILL.md`: daily MDの入力フォーマット定義
- `prompts/analysis_prompt_v2.md`: 出力JSONを入力とする週次分析プロンプト
