# Migrate `normalize_learning_log` to Markdown Input (Improved Plan)

## Goal

`normalize_learning_log` を Notion CSV 直接参照から、`Sessions/Sessions_DB_*.md` を入力とする方式へ移行する。  
`process_sessions_db_export` を前段処理として明示し、責務を分離する。

## Scope

- 対象: `.agent/skills/normalize_learning_log/SKILL.md`
- 対象: `.agent/skills/normalize_learning_log/scripts/normalize.py`
- 削除対象: `.agent/skills/normalize_learning_log/scripts/normalize_from_md.py`
- 非対象: `process_sessions_db_export` 側の処理ロジック変更（インターフェース維持）

## Design Decisions

1. 入力ファイル解決の優先順位
- `--input <path>` が指定された場合はそれを最優先で使用する。
- 未指定時のみ `Sessions/Sessions_DB_*.md` から候補を探索する。
- 自動選択時は `mtime` ではなく、ファイル名の `YYYY-MM-DD_to_YYYY-MM-DD` をパースして最新範囲を選ぶ。

2. 週次範囲の扱い
- 現行の「実行日の今週でフィルタ」ロジックは廃止する。
- 入力Markdownに含まれる `Date` の min/max を period として採用する。

3. Markdown表パースの堅牢化
- 単純 `split('|')` 依存を避け、エスケープ `\|` を壊さないパースを実装する。
- ヘッダ先頭の BOM 除去を行う。
- ヘッダ必須列チェック (`Date`, `Type`, `Deep Score`, `duration (m)f` or `Duration`, `start time`, `end time`, `Notes`) を実施する。
- 解析不能行は件数カウントし、最終ログで警告として表示する。

4. 出力責務
- `normalize.py` の出力は `normalized_data/*.json` のみとする。
- `Sessions_DB_*.md` 生成処理は削除し、`process_sessions_db_export` に一本化する。

## File Changes

### 1) `.agent/skills/normalize_learning_log/SKILL.md` (modify)

- 入力説明を以下に更新:
  - `Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md`（`process_sessions_db_export` 実行後に生成）
  - `daily/daily_YYYY-MM-DD.md`
- 前提条件として以下を明記:
  - 先に `process_sessions_db_export` を実行し、対象週の `Sessions_DB_*.md` を用意すること
- 出力説明を以下に更新:
  - `normalized_data/normalized_data_{start}_to_{end}.json` のみ

### 2) `.agent/skills/normalize_learning_log/scripts/normalize.py` (modify)

- CSV依存 (`csv`, `glob`, `EXPORT_DIR`, `find_latest_sessions_csv`) を削除。
- `find_latest_sessions_md()` を追加:
  - `Sessions/Sessions_DB_*.md` 探索
  - ファイル名の日付範囲で最新判定
- `parse_markdown_table()` を追加:
  - ヘッダ/区切り行検証
  - 行パースと列数整合チェック
  - 必須列検証
- CLI引数対応:
  - `--input <path>` 任意指定
- 正規化フロー:
  - Markdownテーブル → `sessions_by_date`
  - `daily/daily_YYYY-MM-DD.md` と結合
  - `normalized_data_*.json` 出力
- 既存のMarkdown再出力処理を全削除。

### 3) `.agent/skills/normalize_learning_log/scripts/normalize_from_md.py` (delete)

- 実験用スクリプトの役割を `normalize.py` に統合したため削除。

## Verification Plan

## A. Main path (must pass)

1. コマンド:
```bash
python3 /Users/310tea/Documents/Learning_log/.agent/skills/normalize_learning_log/scripts/normalize.py
```
2. 期待結果:
- `Sessions/Sessions_DB_2026-02-16_to_2026-02-22.md` を自動選択できる。
- `normalized_data/normalized_data_2026-02-16_to_2026-02-22.json` が生成される。
- `Sessions` 配下に新規 `Sessions_DB_*.md` を生成しない。

## B. Input selection

1. `--input` 指定時:
```bash
python3 /Users/310tea/Documents/Learning_log/.agent/skills/normalize_learning_log/scripts/normalize.py \
  --input /Users/310tea/Documents/Learning_log/Sessions/Sessions_DB_2026-02-16_to_2026-02-22.md
```
2. 期待結果:
- 指定ファイルが確実に使われる（自動探索を上書き）。

## C. Error handling

1. `Sessions_DB_*.md` が0件:
- 明確なエラーメッセージで終了（終了コード1）。
2. 必須列欠損:
- 欠損列名を表示して終了（終了コード1）。
3. 表形式不正（列数不一致行混在）:
- スキップ件数を警告しつつ、有効行で継続可能なら継続。

## D. Regression check

- 同一週データで旧CSV版の出力JSONと比較し、以下が同等であることを確認:
  - `period.start_date`, `period.end_date`
  - `days[].date`, `sessions[].duration_min`, `sessions[].category`
  - `weekly_summary.total_hours`, `weekly_summary.average_deep_score`

## Rollback Plan

- もし移行後に不整合が出た場合:
1. `normalize.py` をCSV版へ一時的に戻す（git restoreまたはrevert）。
2. `normalize_from_md.py` 削除前コミットを参照して差分確認。
3. 原因修正後に再度Markdown移行を適用。

## Definition of Done

- `SKILL.md` が Markdown入力前提に更新されている。
- `normalize.py` が Markdown入力で安定動作する。
- `normalize.py` が Markdown再出力を行わない。
- `normalize_from_md.py` が削除されている。
- 検証A〜Dが全て完了し、結果を共有済みである。
