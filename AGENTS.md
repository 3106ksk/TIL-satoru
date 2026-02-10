# AGENTS.md

このプロジェクトのファイル命名・整理ルール（学習ログ用）。

## 1) セット管理
- 6週間を1セットとして管理する。
- セットの保存先: `sets/YYYY-MM-DD_to_YYYY-MM-DD/`
- セット内の構成:
  - `daily/`
  - `Sessions/`
  - `weekly/`
  - `weekly_reviews/`（年フォルダ維持: `weekly_reviews/YYYY/`）
- セット境界は「完全に範囲内のみ」含める（開始日・終了日が範囲内のファイルのみ）。
- 既存フォルダのファイルは**コピー**でセットへ集約（元は残す）。

## 2) daily の命名
- 形式: `daily/daily_YYYY-MM-DD.md`
- 日付は本文の `Date:` から抽出（なければタイトル `# 12/22` 等から補完）。
- 同名がある場合は末尾に `_v2`, `_v3` を付与。

## 3) Sessions CSV の命名
- 形式: `Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.csv`
- CSVの `Date` 列の最小/最大日付を範囲として使用。

## 4) Daily Review CSV の命名
- 形式: `daily/Daily_Review_DB_YYYY-MM-DD_to_YYYY-MM-DD.csv`
- CSVの `Date` 列の最小/最大日付を範囲として使用。

## 5) weekly / weekly_reviews
- weekly（通常の週次）
  - 形式: `weekly/weekly_YYYY-MM-DD_to_YYYY-MM-DD.md`
  - 書き出しCSV: `weekly/weekly_YYYY-MM-DD_to_YYYY-MM-DD__v01.csv`
- weekly_reviews（週次レビュー）
  - 形式: `weekly_reviews/YYYY/weekly_YYYY-MM-DD_to_YYYY-MM-DD.md`
  - CSV書き出し: `weekly_reviews/exports/weekly_YYYY-MM-DD_to_YYYY-MM-DD__v01.csv`

## 6) notion_exports
- `notion_exports/` は一時置き場。必要データは上記命名に整形して移動/コピーする。

## 7) ナレッジ蓄積ディレクトリの命名規則

### docs/ （方法論・ガイドライン）
- 形式: `docs/<descriptive_name>.md`
- 人間が参照する恒久的な文書（学習方法論、ガイドライン、フレームワーク等）
- 例: `learning_framework.md`, `debug_verbalization_template.md`

### notes/ （技術メモ）
- 形式: `notes/<category>/<descriptive_name>.md`
- カテゴリ: `rails/`, `javascript/`, `ideas/` 等
- 学習中に得た技術知識、トラブルシューティング、アイデア等
- 例: `notes/rails/activerecord_record_not_found.md`, `notes/ideas/timetable_app_consultation.md`

### prompts/ （AIプロンプトテンプレート）
- 形式: `prompts/<descriptive_name>.md`
- AIとのやり取りで使用するプロンプトテンプレート
- バージョン番号はファイル名に含めない（gitで管理）
- 例: `weekend_review_prompt.md`, `ai_question_format.md`

### outputs/ （成果物・レポート）
- 形式: `outputs/<descriptive_name>.md` または `outputs/<descriptive_name>_YYYY-MM-DD.md`
- Agent生成物以外の成果物・レポート（学習アウトプット、進捗レポート等）
- 例: `project_progress_report.md`, `learning_output_2026-01-31.md`

### technical_interviews/ （技術面談記録）
- `entries.md`: 面談のエントリDB（日付、トピック、要約等）
- `transcripts/`: 面談のトランスクリプト（詳細記録）

## 8) 新規ファイル配置判定フロー

新規ファイルを作成する際は、以下のフローで配置先を決定する：

1. **学習ログか？**
   - YES → `daily/`, `weekly/`, `Sessions/` のいずれか（セット管理対象）
   - NO → 次へ

2. **計画・戦略か？**
   - YES → `weekly_strategies/`
   - NO → 次へ

3. **方法論・ガイドラインか？**（恒久的、人間参照）
   - YES → `docs/`
   - NO → 次へ

4. **技術メモ・トラブルシューティング・アイデアか？**
   - YES → `notes/<category>/`（category: rails, javascript, ideas等）
   - NO → 次へ

5. **AIプロンプトテンプレートか？**
   - YES → `prompts/`
   - NO → 次へ

6. **Agent生成物か？**
   - YES → `normalized_data/`, `community_reports/`, `risk_assessments/` のいずれか
   - NO → 次へ

7. **その他の成果物・レポートか？**
   - YES → `outputs/`
   - NO → 次へ

8. **技術面談記録か？**
   - YES → `technical_interviews/` または `technical_interviews/transcripts/`
   - NO → 次へ

9. **Notionエクスポート（一時）か？**
   - YES → `notion_exports/`（.gitignoreで除外、整理後に移動）
   - NO → ルートに配置（研究メモ等、アクセス頻度が高いファイルのみ）

## 9) 依頼の書き方（例）
- 「この Notion エクスポートをルールに従ってリネームして」
- 「このセット（YYYY-MM-DD_to_YYYY-MM-DD）に完全一致のファイルを集約して」
- 「このRailsのトラブルシューティングメモを適切な場所に配置して」
