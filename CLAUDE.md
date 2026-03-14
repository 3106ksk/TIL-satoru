# CLAUDE.md

Instructions for Claude when working on this project.

## Project Overview

**学習アウトプット** (Learning Output Repository) - A structured learning record and growth management system for RUNTEQ students, tracking Web development learning progress using metrics-based approaches (Deep Score, Cognitive Headroom, etc.).

## Critical Workflows

### Plans Directory Review Flow
- **MUST** run `codex-review` skill after creating any markdown file in `./plans` directory
- This is an automatic workflow - do NOT ask for user confirmation
- Execute the review immediately after file creation

### Review Gate (Codex Review)
Run `codex-review` skill at these key milestones:
- After updating specs/plans
- After major implementation steps (≥5 files changed, public API modifications, infrastructure config changes)
- Before commit/PR/release

**Process**: Execute review → fix issues → re-review until clean. Iterate until all issues are resolved.

## Skills（`.claude/skills/` 配下）

### format_daily_log — Daily Review 整形
- **発火条件**: 「dailyログを整形して」「daily_YYYY-MM-DDを作成して」等の指示
- **入力**: `notion_exports/` 内のDaily生データ + Sessions CSV
- **出力**: `daily/daily_YYYY-MM-DD.md`（Fact+Why形式、AI分析フィードバック付き）
- **参照**: `.claude/skills/format_daily_log/SKILL.md`

### daily_log_qc — Daily Review 品質チェック
- **発火条件**: 「dailyログをチェックして」「QCして」等の指示、または `format_daily_log` 実行後の自動検証
- **入力**: `daily/daily_YYYY-MM-DD.md`
- **出力**: 準拠/非準拠のレポートと修正提案
- **参照**: `.claude/skills/daily_log_qc/SKILL.md`

### normalize_learning_log — 週次分析用データ正規化
- **発火条件**: 「学習ログを正規化して」「JSONデータを生成して」等の指示
- **入力**: `process_sessions_db_export` が生成した `Sessions/Sessions_DB_*.md` + `daily/` 内のMDファイル
- **出力**: `normalized_data/normalized_data_{start}_to_{end}.json`
- **前提**: 実行前に `process_sessions_db_export` でSessions MDを生成しておくこと
- **スクリプト**: `.claude/skills/normalize_learning_log/scripts/normalize.py`
- **参照**: `.claude/skills/normalize_learning_log/SKILL.md`

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

### extract_daily_sessions — Daily Sessions 抽出
- **発火条件**: 「セッション記録を抽出して」「今日のセッションを出力して」等の指示
- **入力**: `notion_exports/` 内のSessions DB CSV + 対象日付
- **出力**: `daily_sessions_record/sessions_YYYY-MM-DD.md`
- **スクリプト**: `.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py`
- **参照**: `.claude/skills/extract_daily_sessions/SKILL.md`

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

### generate_daily_plan — 学習計画（Daily Plan）生成
- **発火条件**: 「学習計画を作成して」「daily planを生成して」「〇月〇日の目標を作って」等の指示
- **入力**: 対象日付 + Day Mode + 学習可能時間 + `weekly_strategies/` + `daily/daily_{前日}.md` + `daily_plan/daily_{前日}_plan.md`
- **出力**: `daily_plan/daily_YYYY-MM-DD_plan.md`
- **参照**: `.claude/skills/generate_daily_plan/SKILL.md`

### create_community_report — コミュニティレポート生成
- **発火条件**: 「コミュニティレポートを作成して」等
- **入力**: 週次戦略JSON + リスク評価MD
- **出力**: `community_reports/YYYY-MM-DD_to_YYYY-MM-DD_report.md`
- **参照**: `.claude/skills/create_community_report/SKILL.md`

## File Management Rules

### Naming Conventions
1. **Use English, lowercase, underscore-separated** (e.g., `daily_log_golden_rules.md`)
2. **Date format: `YYYY-MM-DD`** (ISO 8601)
3. **NO version numbers in filenames** (use git for versioning)
4. **NO spaces in filenames**
5. **Filenames MUST be self-descriptive**

### Directory Structure & File Placement

Refer to [AGENTS.md](AGENTS.md) and [README.md](README.md) for detailed rules. When creating new files, determine placement using this priority flow:

1. **Learning logs** → `daily/`, `weekly/`, `Sessions/` (set-managed)
2. **Plans/strategies** → `weekly_strategies/`
3. **Methodology/guidelines** → `docs/` (permanent, human-readable)
4. **Technical notes** → `notes/<category>/` (rails, javascript, ideas, etc.)
5. **Prompt templates** → `prompts/`
6. **Agent outputs** → `normalized_data/`, `community_reports/`, `risk_assessments/`
7. **Reports/artifacts** → `outputs/`
8. **Technical interviews** → `technical_interviews/`
9. **Agent plan files** → `plans/`
10. **Temporary exports** → `notion_exports/` (.gitignored)

### Set Management (6-Week Cycles)
- One set = 6 weeks
- Set destination: `sets/YYYY-MM-DD_to_YYYY-MM-DD/`
- Include ONLY files fully within date range (start & end dates both within bounds)
- **COPY** files to set directories (keep originals)

## Working Guidelines

### Task Management
- **MUST** use TodoWrite tool when implementing features or making code changes
- Break down work into clear, manageable steps
- Update task status as you proceed (pending → in_progress → completed)
- Keep exactly ONE task in_progress at any time

### Decision Making
- **MUST** use `AskUserQuestion` tool when you need to ask the user for a decision
- Present clear options with descriptions
- Do NOT proceed with assumptions - always confirm when uncertain

### File Operations
- Strictly adhere to existing directory structure and naming conventions
- Place new files in appropriate directories (follow AGENTS.md Section 8 flow)
- NEVER include version numbers in filenames (git handles versioning)
- Read existing files before suggesting modifications

### Git Operations
- Use clear, concise commit messages (English preferred)
- NEVER commit files in `.gitignore` (`notion_exports/`, `.DS_Store`, etc.)
- Follow standard git safety protocols

### Code Quality
- Keep solutions simple and focused - avoid over-engineering
- Only make requested changes - no unsolicited refactoring
- Add comments only where logic is not self-evident
- Prioritize security - avoid common vulnerabilities

## Reference Documents

- [AGENTS.md](AGENTS.md): Detailed naming rules, organization flow, set management
- [README.md](README.md): Repository purpose, directory structure, file placement flow
