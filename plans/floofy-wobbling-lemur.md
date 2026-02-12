# Implementation Plan: Claude Code Skills Directory

## Context

**Why this change is needed:**

The repository currently has `.agent/skills/` for Antigravity framework skills (Python-based automation), but lacks a dedicated location for **Claude Code-specific skills**. The user requested a directory structure for Claude Code skills to store learning-focused, conversational workflows that are distinct from the existing Antigravity automation.

**Problem:**
- No designated location for Claude Code skills
- Existing `.agent/skills/` is framework-specific (Antigravity)
- Skills need to be discoverable and accessible as part of learning content

**Intended outcome:**
Create a clear, simple directory structure at root level (`skills/`) that:
- Stores Claude Code skills for this learning repository
- Maintains clear separation from Antigravity skills
- Follows existing repository conventions (content visible, tools hidden)
- Integrates seamlessly with documentation and workflows

## Recommended Approach

### Directory Structure

Create `skills/` at repository root with the following structure:

```
/学習アウトプット/
├── skills/                         # Claude Code skills (NEW)
│   ├── README.md                   # Skill directory guide
│   └── <skill_name>/               # Individual skills
│       ├── SKILL.md                # Required: skill definition
│       ├── scripts/                # Optional: executable code
│       ├── references/             # Optional: reference docs
│       └── assets/                 # Optional: resources
```

**Rationale for root-level placement:**
1. **Consistency**: Content directories (docs/, notes/, prompts/) are at root - skills follow same pattern
2. **Discoverability**: Visible and immediately accessible, not buried in hidden directories
3. **Repository philosophy**: Root = content, hidden directories = system config/tooling
4. **User-facing**: Claude Code skills are part of the learning workflow, not system automation

### Clear Separation

| Directory | Purpose | Type |
|-----------|---------|------|
| `skills/` | Claude Code skills (conversational, learning-focused) | User content |
| `.agent/skills/` | Antigravity framework skills (Python automation) | System tooling |
| `.claude/skill-creator-best/` | System skill for creating skills | System tooling |

## Critical Files to Modify

### 1. [README.md](README.md)
**Update:** Add `skills/` to directory structure section (line 11)

**Change:**
```markdown
/学習アウトプット/
├── .agent/skills/              # Agent用スキル定義
├── .gitignore                  # Git除外設定
├── AGENTS.md                   # Agent動作ルール・命名規則
├── README.md                   # このファイル
├── skills/                     # Claude Codeスキル定義（学習特化ワークフロー）  ← ADD
```

**Update:** Add to file placement flow section (line 53-62)

**Add:**
```markdown
- **Claude Codeスキル**: `skills/<skill_name>/` に配置
```

### 2. [AGENTS.md](AGENTS.md)
**Update:** Add to Section 8 "新規ファイル配置判定フロー" (after step 9, before final fallback)

**Add new step:**
```markdown
10. **Claude Codeスキルか？**
    - YES → `skills/<skill_name>/`
    - NO → ルートに配置（研究メモ等、アクセス頻度が高いファイルのみ）
```

**Decision criteria:**
- Reusable Claude Code workflows/procedures → `skills/`
- Project-specific learning automation → `skills/`
- Generic agent automation → `.agent/skills/` (Antigravity)

### 3. [CLAUDE.md](CLAUDE.md)
**Update:** Add to file placement priority flow (line 37-46)

**Add after line 45 (before "10. Temporary exports"):**
```markdown
10. **Claude Code skills** → `skills/<skill_name>/`
11. **Temporary exports** → `notion_exports/` (.gitignored)
```

### 4. [skills/README.md](skills/README.md) (NEW)
**Create:** Comprehensive guide for skills directory

**Content:**
```markdown
# Claude Code Skills

This directory contains Claude Code skills specific to this learning repository.

## Purpose

Claude Code skills are conversational, flexible workflows designed for learning-specific tasks in this repository. They differ from Antigravity skills (`.agent/skills/`) which are Python-based automation tools.

## Structure

Each skill follows the standard Claude Code skill format:

```
skills/
└── <skill_name>/
    ├── SKILL.md              # Required: YAML frontmatter + instructions
    ├── scripts/              # Optional: executable scripts
    ├── references/           # Optional: reference documentation
    └── assets/               # Optional: output resources/templates
```

### SKILL.md Format

```yaml
---
name: skill_name
description: Brief description of what this skill does and when to use it
---

# Skill Name

Detailed instructions for Claude on how to execute this skill.

## What This Skill Does

Clear explanation of the skill's purpose and output.

## How to Use

Step-by-step usage instructions.

## Scripts (if applicable)

- `scripts/example.py`: Description of what the script does
```

## Skill Types

### Learning Workflow Skills
Skills that automate learning-specific workflows:
- Log analysis and pattern identification
- Weekly review generation
- Metrics tracking (Deep Score, Cognitive Headroom)
- Progress visualization

### Repository Management Skills
Skills that maintain and organize repository structure:
- File organization and renaming
- Set management automation
- Documentation generation

## Difference from .agent/skills/

| Aspect | `skills/` | `.agent/skills/` |
|--------|-----------|------------------|
| **Framework** | Claude Code | Antigravity |
| **Style** | Conversational, flexible | Python automation |
| **Scope** | This repository only | Can be general purpose |
| **Visibility** | Root level (content) | Hidden directory (tooling) |
| **Use case** | Learning workflows | System automation |

## Creating New Skills

Use the `skill-creator` skill in `.claude/skill-creator-best/` to create new skills, or manually create following the structure above.

## Example Skills (Future)

Potential skills for this repository:
- `learning_log_analyzer`: Analyze daily logs for patterns and insights
- `weekly_review_generator`: Generate comprehensive weekly reviews
- `deep_score_tracker`: Track and visualize Deep Score metrics over time
- `set_archiver`: Automate 6-week set archival process
- `interview_transcript_organizer`: Process and organize technical interview transcripts

## Best Practices

1. **No secrets**: Never include API keys or sensitive data in skills
2. **Document dependencies**: List required packages/tools in SKILL.md
3. **Test before committing**: Verify scripts work as expected
4. **Use absolute paths**: Reference repository files with absolute paths
5. **Follow naming conventions**: Lowercase, underscore-separated names
```

### 5. [.gitignore](.gitignore)
**No changes needed** - `skills/` should be tracked in git like other content directories

## Implementation Steps

1. **Create `skills/` directory** at repository root
2. **Create `skills/README.md`** with comprehensive guide (content above)
3. **Update README.md**:
   - Add `skills/` to directory structure (line 11)
   - Add skill placement rule to flow section (after line 61)
4. **Update AGENTS.md**:
   - Add step 10 to Section 8 file placement flow (after line 105)
5. **Update CLAUDE.md**:
   - Add skill placement to priority flow (insert at line 45, renumber subsequent items)

## Verification

After implementation, verify:

1. **Directory created**: `ls -la /Users/310tea/Documents/学習アウトプット/skills/`
2. **README exists**: `cat /Users/310tea/Documents/学習アウトプット/skills/README.md`
3. **Documentation updated**: Check README.md, AGENTS.md, CLAUDE.md contain new references
4. **Git tracking**: `git status` shows new files as untracked (ready to commit)
5. **Test skill creation**: Create a simple test skill to validate structure works

## Future Considerations

- **Migration**: If future skills in `.claude/` are learning-specific, consider moving to `skills/`
- **Integration**: Skills in `skills/` do NOT trigger automatic codex-review (unlike `plans/`)
- **Documentation**: Keep skills/README.md updated as new skills are added
- **Naming**: Maintain consistency with repository naming conventions (lowercase, underscores)
