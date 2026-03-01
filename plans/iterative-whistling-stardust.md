# `.claude/skills` を `.agent/skills` の最新版に同期する設計書

## Context

`.agent/skills/` が開発中のアクティブなスキルディレクトリとして進化してきた一方、`.claude/skills/` は古いスナップショットのまま残っている。Claude Code が参照するのは `.claude/skills/` であるため、最新のスキル定義・スクリプトを `.agent/skills/` から `.claude/skills/` へ同期し、一貫性を確保する。

> 運用メモ: 現行スキル実装では Sessions 変換の出力は `Sessions_DB_*.md` を前提にしている（`process_sessions_db_export` / `normalize_learning_log`）。本同期では **実装に合わせて同期** し、AGENTS.md のCSV命名規約との整合は別タスクで解消する。

---

## 現状の差分サマリ

| カテゴリ | スキル名 | 対応 |
|----------|----------|------|
| **新規追加（5件）** | `import_weekly_review` | `.agent` → `.claude` へコピー |
| | `organize_interview_transcript` | `.agent` → `.claude` へコピー |
| | `process_sessions_db_export` | `.agent` → `.claude` へコピー |
| | `weekly_planning_assistant` | `.agent` → `.claude` へコピー |
| | `create_community_report` | `.agent` → `.claude` へコピー |
| **内容更新（1件）** | `normalize_learning_log` | SKILL.md + normalize.py を上書き |
| **変更なし（5件）** | `daily_log_qc` | 対応不要（同一） |
| | `format_daily_log` | 対応不要（同一） |
| | `generate-runteq-report` | 対応不要（同一） |
| | `generate_daily_plan` | 対応不要（同一） |
| | `skill-creator-best` | 対応不要（同一） |

---

## 実施手順

### Step 1: 新規スキル5件のコピー

`.agent/skills/` から `.claude/skills/` へディレクトリごとコピー。

| スキル | コピー対象ファイル |
|--------|-------------------|
| `import_weekly_review/` | `SKILL.md`, `scripts/process_weekly_export.py` |
| `organize_interview_transcript/` | `SKILL.md` |
| `process_sessions_db_export/` | `SKILL.md`, `scripts/process_sessions.py` |
| `weekly_planning_assistant/` | `SKILL.md` |
| `create_community_report/` | `SKILL.md` |

### Step 2: normalize_learning_log の更新

以下のファイルを `.agent/skills/` の最新版で上書き。

| ファイル | 主な変更点 |
|----------|-----------|
| `SKILL.md` | 入力ソースが CSV → Sessions MD に変更。`process_sessions_db_export` との2ステップワークフロー明記 |
| `scripts/normalize.py` | 369行 → 426行。MD入力対応、日次データ抽出の大幅拡充（stats/plan/feedback/learning_record追加）、CSV→MD生成ロジック削除 |

**変更の要点:**
- **入力パイプライン**: `notion_exports/` の生CSV → `Sessions/` の前処理済MDに変更
- **出力JSON構造**: day_obj が 2フィールド → 7フィールドに拡充
- **責務分離**: CSV→MD変換は `process_sessions_db_export` に委譲

### Step 3: パス参照の修正

`.agent/skills/` からコピーしたファイル内のパス参照を `.claude/skills/` に統一する。

対象ファイル:
- `.claude/skills/import_weekly_review/SKILL.md` 内の実行コマンド説明（`.agent/skills/...`）を `.claude/skills/...` に置換
- `.claude/skills/process_sessions_db_export/SKILL.md` 内の実行コマンド説明（`.agent/skills/...`）を `.claude/skills/...` に置換
- `.claude/skills/normalize_learning_log/SKILL.md` 内の実行コマンド説明・参照パス（`.agent/skills/...`）を `.claude/skills/...` に置換
- `.claude/skills/normalize_learning_log/scripts/normalize.py` はベースディレクトリが `/Users/310tea/Documents/Learning_log` 固定であり、`skills` パス依存がないことを確認（変更不要）

修正方針:
- **説明コメント/参照パスはすべて `.claude/skills` 基準に統一**
- 実行ロジック（Pythonスクリプト本体）は、機能要件に影響しない限り変更しない

### Step 4: CLAUDE.md のスキル一覧更新

`CLAUDE.md` の `## Skills` セクションに新規5スキルの記載を追加。

追加するエントリ:
```markdown
### import_weekly_review — Weekly Review CSV取込
- **発火条件**: 「Weekly Reviewを取り込んで」等
- **入力**: `notion_exports/` 内のWeekly Review CSV
- **出力**: `weekly/weekly_YYYY-MM-DD_to_YYYY-MM-DD.md`
- **参照**: `.claude/skills/import_weekly_review/SKILL.md`

### organize_interview_transcript — 面接記録整理
- **発火条件**: 「面接ファイルを整理して」等
- **入力**: 面接トランスクリプトファイル
- **出力**: `technical_interviews/transcripts/YYYY-MM-DD_<Topic>.<ext>`
- **参照**: `.claude/skills/organize_interview_transcript/SKILL.md`

### process_sessions_db_export — Sessions CSV→MD変換（現行実装）
- **発火条件**: 「SessionsのCSVを処理して」等
- **入力**: `notion_exports/` 内のSessions DB CSV
- **出力**: `Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md`
- **参照**: `.claude/skills/process_sessions_db_export/SKILL.md`

### weekly_planning_assistant — 週次戦略策定
- **発火条件**: 「今週の戦略を作って」等
- **入力**: 週次戦略設計入力 + 前週データ
- **出力**: `weekly_strategies/` JSON + `risk_assessments/` MD
- **参照**: `.claude/skills/weekly_planning_assistant/SKILL.md`

### create_community_report — コミュニティレポート生成
- **発火条件**: 「コミュニティレポートを作成して」等
- **入力**: 週次戦略JSON + リスク評価MD
- **出力**: `community_reports/YYYY-MM-DD_to_YYYY-MM-DD_report.md`
- **参照**: `.claude/skills/create_community_report/SKILL.md`
```

また、既存の `normalize_learning_log` の記述を更新し、`process_sessions_db_export` との依存関係を明記する。

注記として `normalize_learning_log` の入力説明を以下に更新する:
- 旧: `notion_exports/` の Sessions CSV を直接入力
- 新: `process_sessions_db_export` が生成した `Sessions/Sessions_DB_*.md` を入力

---

## 対象ファイル一覧

### 新規作成
- `.claude/skills/import_weekly_review/SKILL.md`
- `.claude/skills/import_weekly_review/scripts/process_weekly_export.py`
- `.claude/skills/organize_interview_transcript/SKILL.md`
- `.claude/skills/process_sessions_db_export/SKILL.md`
- `.claude/skills/process_sessions_db_export/scripts/process_sessions.py`
- `.claude/skills/weekly_planning_assistant/SKILL.md`
- `.claude/skills/create_community_report/SKILL.md`

### 上書き更新
- `.claude/skills/normalize_learning_log/SKILL.md`
- `.claude/skills/normalize_learning_log/scripts/normalize.py`

### 編集
- `CLAUDE.md`（スキル一覧セクション）

### 変更なし（確認済み）
- `.claude/skills/daily_log_qc/SKILL.md`
- `.claude/skills/format_daily_log/SKILL.md`
- `.claude/skills/generate-runteq-report/` (SKILL.md + script)
- `.claude/skills/generate_daily_plan/SKILL.md`
- `.claude/skills/skill-creator-best/` (全ファイル)

---

## 検証方法

1. **ファイル存在確認**: `.claude/skills/` 配下に全11スキルのディレクトリとファイルが存在することを `ls -R` で確認
2. **説明コメントのパス統一確認**: `rg -n "\.agent/skills" .claude/skills/*/SKILL.md` が 0件であることを確認
3. **差分確認**: `diff -r .claude/skills/ .agent/skills/` を実行し、差分が「Step 3 で意図したパス文字列差分 + CLAUDE.md追記に伴う参照差分」のみであることを確認
4. **CLAUDE.md 整合性**: CLAUDE.md に記載された全スキルの参照パスが実在することを確認
5. **スクリプト実行テスト**:
   - `python3 .claude/skills/normalize_learning_log/scripts/normalize.py --help`
   - `python3 .claude/skills/process_sessions_db_export/scripts/process_sessions.py --help`
   がいずれも正常終了することを確認
