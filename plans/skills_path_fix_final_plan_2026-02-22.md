# Skills修正 + Sessions CSV自動抽出安定化 最終プラン（2026-02-22）

## 1. 目的
- `Sessions DB` CSV から「今週分」を抽出して Markdown 化する運用を、次回以降も迷わず再実行できる状態にする。
- 旧パス（`/Users/310tea/Documents/学習アウトプット`、`.claude/...`）由来の不具合を解消する。
- `notion_exports/ExportBlock-.../Sessions/...` のようなネスト構造でも CSV 自動検出できるようにする。

## 2. 修正対象（確定）
- `.agent/skills/import_weekly_review/SKILL.md`
- `.agent/skills/import_weekly_review/scripts/process_weekly_export.py`
- `.agent/skills/normalize_learning_log/SKILL.md`
- `.agent/skills/normalize_learning_log/scripts/normalize.py`
- `.agent/skills/process_sessions_db_export/SKILL.md`
- `.agent/skills/organize_interview_transcript/SKILL.md`
- `.agent/skills/weekly_planning_assistant/SKILL.md`

## 3. 修正対象外（明示）
- `.agent/skills/process_sessions_db_export/scripts/process_sessions.py`
  - 理由: 旧絶対パスを内部で持っておらず、引数ベースで動作しているため。

## 4. 実装方針
1. 旧ルート名置換
- `学習アウトプット` → `Learning_log` を上記対象ファイルで修正。

2. 旧スキルパス置換
- `.claude/...` → `.agent/skills/...` を `normalize_learning_log/SKILL.md` で修正。

3. `normalize.py` のCSV探索強化
- `find_latest_sessions_csv()` を再帰探索に変更。
- 例: `notion_exports/**/Sessions DB*.csv` を `recursive=True` で探索し、更新時刻最新を採用。

4. スキル手順の明文化
- `process_sessions_db_export/SKILL.md` に「ExportBlock 配下を含むネストCSVの指定方法」を追記。
- 実行コマンド例を現行パスで統一。

## 5. 改善済みチェックポイント
### A. 事前チェック
- `rg` で旧パス残存箇所を一覧化し、修正対象を固定。
- 「修正対象外ファイル」を先に宣言し、不要編集を防止。

### B. 実装チェック
- 各SKILL.mdのコマンド例が実際のディレクトリ構成と一致していること。
- `normalize.py` の探索がトップ階層限定になっていないこと（`**` 再帰探索）。
- 例外時メッセージが探索対象（`notion_exports` 配下再帰）を示していること。

### C. 検証チェック（重要）
1. 静的検証
- `.agent/skills` 配下の `.md/.py` から `学習アウトプット` と `.claude/` が消えていることを確認。

2. 機能検証
- `notion_exports/ExportBlock-.../Sessions/` 配下にある実CSVを `normalize.py` が検出できること。
- 実行で「対象週に該当データあり/なし」の両ケースで異常終了しないこと（想定メッセージを確認）。

3. ドキュメント検証
- `process_sessions_db_export/SKILL.md` の手順だけで、次回同等作業が再現できること（人間が読んで実行可能）。

## 6. 完了条件（Definition of Done）
- 旧パス/旧参照の残存ゼロ。
- `normalize.py` がネストCSVを自動検出できる。
- Sessions処理スキルの手順が現行構成で自己完結している。
- 上記を確認した検証ログ（コマンド結果要約）を残して完了報告。
