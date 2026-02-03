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

## 7) 依頼の書き方（例）
- 「この Notion エクスポートをルールに従ってリネームして」
- 「このセット（YYYY-MM-DD_to_YYYY-MM-DD）に完全一致のファイルを集約して」
