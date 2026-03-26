# Plan: Sessions形式の選定とパイプライン整備

## Context

`normalized_data/` のJSON生成パイプラインにおいて、`daily_sessions_record/` の日次ログをどの中間形式で `Sessions/` に配置すべきかを判断する必要があった。

現在2つの形式が存在する：
- **Sessions_DB形式**: `Sessions_DB_2026-03-02_to_2026-03-08.md` — フラットなMarkdownテーブル
- **Sessions_weekly形式**: `Sessions_weekly_2026-03-08_to_2026-03-14.md` — 日別セクション構造（今回作成したもの）

## 結論: Sessions_DB形式が唯一の正解

`normalize.py` は以下の**特定のカラム名・フォーマット**を要求する：

| 要件 | Sessions_DB | Sessions_weekly |
|------|:-----------:|:---------------:|
| `start time` (Notion形式: "March 3, 2026 7:29 AM (GMT+9)") | OK | NG（"7:30"のみ） |
| `end time` (Notion形式) | OK | NG |
| `duration (m)f` (整数) | OK | NG（"65m"形式） |
| `Notes` カラム内に`<br>`区切り | OK | NG（別セクション） |
| `Date`, `Type`, `Deep Score` カラム | OK | NG（カラム名が異なる） |

**Sessions_weekly形式はnormalize.pyと互換性がない。** Sessions_DB形式のみがパイプラインに適合する。

## 既存の変換スクリプト: merge_daily_sessions.py

重要な発見として、**この変換を行うスクリプトが既に存在する**。

- **パス**: [merge_daily_sessions.py](.claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py)
- **機能**: `daily_sessions_record/sessions_*.md` → `Sessions/Sessions_DB_*.md` への変換
- **処理内容**:
  - 短縮時刻 ("7:29") → Notion形式 ("March 3, 2026 7:29 AM (GMT+9)")
  - Duration ("44m", "1h 27m") → 整数分
  - Notes `### #N` セクション → `<br>`区切りインライン
  - WeekKey自動算出、全23カラムの生成

### 実行コマンド

```bash
# Step 1: daily_sessions_record → Sessions_DB 変換
python3 .claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py 2026-03-08 2026-03-14

# Step 2: Sessions_DB → normalized JSON
python3 .claude/skills/normalize_learning_log/scripts/normalize.py \
  --input Sessions/Sessions_DB_2026-03-08_to_2026-03-14.md
```

## 実施事項

### 1. 今週分のSessions_DB生成 & JSON正規化
- `merge_daily_sessions.py 2026-03-08 2026-03-14` を実行
- 生成された `Sessions_DB_2026-03-08_to_2026-03-14.md` の内容を検証
- `normalize.py --input` で JSON 生成
- 出力JSONの構造・日数・セッション数を検証

### 2. Sessions_weekly ファイルの扱い
- `Sessions_weekly_2026-03-08_to_2026-03-14.md` は**人間向けの閲覧用**として残す
- パイプラインには使用しない
- 今後作成する場合も、パイプライン用途には `merge_daily_sessions.py` を使用

### 3. スキルドキュメント更新

**[normalize_learning_log/SKILL.md](.claude/skills/normalize_learning_log/SKILL.md)**:
- Notion CSV経由のPath A記述を削除
- 唯一のパスとして `daily_sessions_record` → `merge_daily_sessions.py` → Sessions_DB → normalize.py を記載

**[process_sessions_db_export/SKILL.md](.claude/skills/process_sessions_db_export/SKILL.md)**:
- `process_sessions.py`（Notion CSV変換）の記述を廃止・削除
- `merge_daily_sessions.py` を唯一の入力方法として書き換え
- Usage/Exampleセクションを `merge_daily_sessions.py` ベースに更新

## 検証方法

1. `merge_daily_sessions.py` 実行後、Sessions_DB ファイルが生成されることを確認
2. 出力ファイルのカラム数（23列）、行数（日次ファイルのセッション合計と一致）を確認
3. `normalize.py` が正常にJSONを出力し、`days` 配列に対象日が含まれることを確認
4. 既存の `normalized_data_2026-03-03_to_2026-03-08.json` と構造を比較して整合性を確認

## 対象ファイル

| ファイル | 操作 |
|---------|------|
| `.claude/skills/process_sessions_db_export/scripts/merge_daily_sessions.py` | 実行（変更なし） |
| `.claude/skills/normalize_learning_log/scripts/normalize.py` | 実行（変更なし） |
| `.claude/skills/normalize_learning_log/SKILL.md` | ドキュメント更新 |
| `.claude/skills/process_sessions_db_export/SKILL.md` | ドキュメント更新 |
| `Sessions/Sessions_DB_2026-03-08_to_2026-03-14.md` | 新規生成 |
| `normalized_data/normalized_data_2026-03-08_to_2026-03-14.json` | 新規生成 |
