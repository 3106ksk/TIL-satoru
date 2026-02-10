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
