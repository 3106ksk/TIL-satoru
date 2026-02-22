# Repository Separation Strategy: Learning Logs vs. General Outputs

## Executive Summary

Split the current "学習アウトプット" repository into two focused projects:

1. **学習アウトプット** (Learning Logs) - RUNTEQ-specific metrics tracking system
2. **アウトプット集** (Outputs Collection) - Reusable articles, guides, and app ideas

This separation will reduce clutter, improve maintainability, and create clearer boundaries between time-bound learning records and permanent knowledge artifacts.

---

## 1. Separation Rationale

### Current Problems
- **Mixed Purpose**: Learning metrics tracking (temporal) + general knowledge (permanent)
- **Clutter**: 31 root-level items, unclear file categorization
- **Cognitive Load**: Users must filter RUNTEQ-specific vs. reusable content
- **Maintenance Burden**: Updates to general docs pollute learning log history

### Benefits of Separation
- **Clear Context**: Each project has single, focused purpose
- **Better Navigation**: Easier to find relevant content
- **Git History Clarity**: Commits reflect actual project purpose
- **Reusability**: General docs can be referenced across projects

---

## 2. Project Boundary Definitions

### Project A: 学習アウトプット (Learning Logs)
**Purpose**: RUNTEQ learning progress tracking using metrics-based approaches

**Scope**:
- Time-bound learning records (daily, weekly, Sessions)
- RUNTEQ-specific metrics (Deep Score, Cognitive Headroom)
- Learning analytics (normalized data, community reports)
- RUNTEQ-specific technical interviews
- Agent skills for log processing
- Learning-specific prompts and workflows

**Retention Criteria**:
- Contains dates or references specific learning periods
- Generates/consumes metrics data
- Part of RUNTEQ curriculum journey
- Used by agent skills for analysis

---

### Project B: アウトプット集 (Outputs Collection)
**Purpose**: Reusable knowledge artifacts for web development

**Scope**:
- Published articles and essays
- App ideas and project specs
- General development methodologies
- Technical research and references
- Reusable prompt templates
- General technical interviews

**Retention Criteria**:
- Context-independent, reusable across projects
- No specific dates or RUNTEQ references
- General web development knowledge
- Can be referenced by future projects

---

## 3. File Migration Map

### Files Moving to "アウトプット集" (23 files)

#### Articles/Essays (3 files)
```
記事.md → articles/mini_app_development_reflection.md
notes/ai_learning_methodology.md → articles/ai_era_learning_theory.md
infrastructure_tips_1.md → guides/infrastructure_tips_for_beginners.md
```

#### App Ideas (6 files)
```
notes/app_ideas/learning_tips_consultation.md → app_ideas/learning_tips_consultation.md
notes/app_ideas/gochi_fit.md → app_ideas/gochi_fit.md
notes/app_ideas/reappraisal_app.md → app_ideas/reappraisal_app.md
notes/app_ideas/consultation_tech_research_prompt.md → app_ideas/consultation_tech_research_prompt.md
notes/app_ideas/timetable_app_consultation.md → app_ideas/timetable_app_consultation.md
相談.md → DELETE (duplicate of learning_tips_consultation.md)
```

#### General Methodologies (6 files)
```
docs/app_development_guide.md → guides/app_development_guide.md
docs/mvp_definitions_and_tips.md → guides/mvp_definitions_and_tips.md
docs/learning_framework.md → guides/learning_framework.md
docs/debug_verbalization_template.md → guides/debug_verbalization_template.md
docs/implementation_process_guide.md → guides/implementation_process_guide.md
docs/runteq_engineer_skills.md → guides/runteq_engineer_skills.md
```

#### General Prompts (3 files)
```
prompts/tech_selection_pagination.md → prompts/tech_selection_pagination.md
prompts/ai_question_format.md → prompts/ai_question_format.md
prompts/log_reading_practice.md → prompts/log_reading_practice.md
```

#### General Technical Interviews (4 files)
```
technical_interviews/transcripts/2026-02-03_Githubドキュメント読み解き方.md → interviews/github_docs_reading.md
technical_interviews/transcripts/2026-02-05_Rails_CurrentUser_Helper_Method.md → interviews/rails_current_user_helper.md
technical_interviews/transcripts/2026-02-06_Gemドキュメントの読み方.md → interviews/gem_docs_reading.md
technical_interviews/transcripts/2026-02-13_アプリアイデア構築方法.md → interviews/app_idea_construction.md
```

---

### Files Remaining in "学習アウトプット" (Core Learning System)

#### Learning Logs (Active)
- `daily/` (35+ files) - Daily reviews with metrics
- `weekly/` (4 files) - Weekly summaries
- `Sessions/` (11 files) - Session tracking CSVs
- `weekly_reviews/` - Structured weekly reviews
- `weekly_strategies/` - Weekly plans

#### Analytics & Reports
- `normalized_data/` - JSON data for analysis
- `community_reports/` - Learning community reports
- `risk_assessments/` - Learning risk analysis
- `sets/` - 6-week learning archives

#### Learning-Specific Docs (6 files)
- `docs/daily_log_golden_rules.md`
- `docs/daily_log_operations.md`
- `docs/weekly_review_workflow.md`
- `docs/reflection_metrics.md`

#### Learning-Specific Prompts (4 files)
- `prompts/gap_analysis_prompt.md`
- `prompts/weekly_strategy_prompt.md`
- `prompts/weekend_review_prompt.md`
- `prompts/analysis_prompt_v2.md`

#### RUNTEQ-Specific Interviews (2 files)
- `technical_interviews/transcripts/2026-02-12_ミニアプリ開発と卒業制作の方向性相談.md`
- `technical_interviews/transcripts/2026-02-15_ミニアプリ開発の技術選定とAI機能相談.md`

#### Agent Infrastructure
- `.agent/skills/` - All 9 skills (format_daily_log, normalize_learning_log, etc.)
- `.claude/skills/` - Claude-specific skills
- `plans/` - Agent planning outputs

#### Configuration
- `README.md`, `AGENTS.md`, `CLAUDE.md`
- `.gitignore`
- `notion_exports/` (temporary)

---

## 4. New Project Structure: "アウトプット集"

```
/アウトプット集/
├── README.md                     # Project overview
├── .gitignore
│
├── articles/                     # Published essays
│   ├── mini_app_development_reflection.md
│   ├── ai_era_learning_theory.md
│   └── ...
│
├── guides/                       # Development methodologies
│   ├── app_development_guide.md
│   ├── mvp_definitions_and_tips.md
│   ├── learning_framework.md
│   ├── debug_verbalization_template.md
│   ├── implementation_process_guide.md
│   ├── runteq_engineer_skills.md
│   └── infrastructure_tips_for_beginners.md
│
├── app_ideas/                    # Project specs
│   ├── learning_tips_consultation.md
│   ├── gochi_fit.md
│   ├── reappraisal_app.md
│   ├── consultation_tech_research_prompt.md
│   └── timetable_app_consultation.md
│
├── prompts/                      # General prompt templates
│   ├── tech_selection_pagination.md
│   ├── ai_question_format.md
│   └── log_reading_practice.md
│
├── interviews/                   # Technical consultations
│   ├── github_docs_reading.md
│   ├── rails_current_user_helper.md
│   ├── gem_docs_reading.md
│   └── app_idea_construction.md
│
└── notes/                        # Technical memos
    ├── rails/
    │   ├── activerecord_record_not_found.md
    │   └── mount_engine_routing.md
    └── javascript/
        └── promise_tutorial.md
```

---

## 5. Migration Strategy

### Phase 1: Create New Repository (Day 1)

#### Step 1.1: Initialize New Project
```bash
cd ~/Documents
mkdir アウトプット集
cd アウトプット集
git init
```

#### Step 1.2: Create Directory Structure
```bash
mkdir -p articles guides app_ideas prompts interviews notes/rails notes/javascript
```

#### Step 1.3: Create README.md
Content should include:
- Project purpose: "Reusable knowledge artifacts for web development"
- Directory structure
- Naming conventions (English, lowercase, underscores)
- Contributing guidelines

#### Step 1.4: Create .gitignore
```
.DS_Store
*.swp
*.swo
.vscode/
.idea/
```

---

### Phase 2: Copy Files with Git History Preservation (Day 1-2)

Use `git log --follow` to preserve authorship and history for important files.

#### Step 2.1: Copy Articles
```bash
cd ~/Documents/学習アウトプット

# Get file history
git log --follow -- 記事.md > /tmp/記事_history.txt

# Copy to new repo
cp 記事.md ~/Documents/アウトプット集/articles/mini_app_development_reflection.md
cp notes/ai_learning_methodology.md ~/Documents/アウトプット集/articles/ai_era_learning_theory.md
cp infrastructure_tips_1.md ~/Documents/アウトプット集/guides/infrastructure_tips_for_beginners.md
```

#### Step 2.2: Copy App Ideas
```bash
cp notes/app_ideas/*.md ~/Documents/アウトプット集/app_ideas/
```

#### Step 2.3: Copy General Guides
```bash
cp docs/app_development_guide.md ~/Documents/アウトプット集/guides/
cp docs/mvp_definitions_and_tips.md ~/Documents/アウトプット集/guides/
cp docs/learning_framework.md ~/Documents/アウトプット集/guides/
cp docs/debug_verbalization_template.md ~/Documents/アウトプット集/guides/
cp docs/implementation_process_guide.md ~/Documents/アウトプット集/guides/
cp docs/runteq_engineer_skills.md ~/Documents/アウトプット集/guides/
```

#### Step 2.4: Copy General Prompts
```bash
cp prompts/tech_selection_pagination.md ~/Documents/アウトプット集/prompts/
cp prompts/ai_question_format.md ~/Documents/アウトプット集/prompts/
cp prompts/log_reading_practice.md ~/Documents/アウトプット集/prompts/
```

#### Step 2.5: Copy General Interviews
```bash
cp technical_interviews/transcripts/2026-02-03_Githubドキュメント読み解き方.md \
   ~/Documents/アウトプット集/interviews/github_docs_reading.md

cp technical_interviews/transcripts/2026-02-05_Rails_CurrentUser_Helper_Method.md \
   ~/Documents/アウトプット集/interviews/rails_current_user_helper.md

cp technical_interviews/transcripts/2026-02-06_Gemドキュメントの読み方.md \
   ~/Documents/アウトプット集/interviews/gem_docs_reading.md

cp technical_interviews/transcripts/2026-02-13_アプリアイデア構築方法.md \
   ~/Documents/アウトプット集/interviews/app_idea_construction.md
```

#### Step 2.6: Copy Technical Notes
```bash
cp -r notes/rails ~/Documents/アウトプット集/notes/
cp -r notes/javascript ~/Documents/アウトプット集/notes/
```

---

### Phase 3: Cleanup Old Repository (Day 2)

#### Step 3.1: Remove Migrated Files
```bash
cd ~/Documents/学習アウトプット

# Remove articles
git rm 記事.md infrastructure_tips_1.md 相談.md

# Remove general guides from docs/
git rm docs/app_development_guide.md
git rm docs/mvp_definitions_and_tips.md
git rm docs/learning_framework.md
git rm docs/debug_verbalization_template.md
git rm docs/implementation_process_guide.md
git rm docs/runteq_engineer_skills.md

# Remove general prompts
git rm prompts/tech_selection_pagination.md
git rm prompts/ai_question_format.md
git rm prompts/log_reading_practice.md

# Remove app ideas directory
git rm -r notes/app_ideas/

# Remove general technical interviews
git rm technical_interviews/transcripts/2026-02-03_Githubドキュメント読み解き方.md
git rm technical_interviews/transcripts/2026-02-05_Rails_CurrentUser_Helper_Method.md
git rm technical_interviews/transcripts/2026-02-06_Gemドキュメントの読み方.md
git rm technical_interviews/transcripts/2026-02-13_アプリアイデア構築方法.md

# Remove general technical notes (keep notes/ideas/ for learning-specific ideas)
git rm -r notes/rails/
git rm -r notes/javascript/
git rm notes/ai_learning_methodology.md
```

#### Step 3.2: Update README.md
Update README to reflect the focused scope:
- Remove references to general guides
- Emphasize RUNTEQ-specific learning tracking
- Update directory structure documentation

#### Step 3.3: Update AGENTS.md
Remove examples and references to moved files:
- Remove `notes/ideas/` from examples (keep `notes/ideas/agent_skill_design_memo.md`)
- Clarify that `docs/` is for learning-log-specific docs only

#### Step 3.4: Update CLAUDE.md
No changes needed - skills remain in place.

---

### Phase 4: Commit Changes (Day 2)

#### Step 4.1: Commit New Repository
```bash
cd ~/Documents/アウトプット集
git add .
git commit -m "Initial commit: Web development outputs collection

- Articles: Mini-app development reflection, AI learning theory
- Guides: App development, MVP definitions, learning frameworks
- App Ideas: 5 project specs with consultation notes
- Prompts: General-purpose templates for tech research
- Interviews: General technical consultation transcripts
- Notes: Rails and JavaScript technical memos

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Step 4.2: Commit Old Repository Cleanup
```bash
cd ~/Documents/学習アウトプット
git add -A
git commit -m "Refactor: Separate general outputs to new repository

Moved 23 files to 'アウトプット集' repository:
- 3 articles/essays
- 6 app ideas
- 6 general methodologies
- 3 general prompts
- 4 general technical interviews
- Technical notes (rails, javascript)

This repository now focuses exclusively on RUNTEQ learning log tracking.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## 6. Naming & Organization Rules

### "アウトプット集" Naming Conventions

#### Files
- **Format**: `lowercase_with_underscores.md`
- **No dates**: Unless article publication date is meaningful
- **Descriptive**: Name should indicate content at a glance
- **English preferred**: For better compatibility

#### Example Mappings
```
Bad                                  Good
-----------------------------------  -------------------------------------
記事.md                              mini_app_development_reflection.md
相談.md                              (delete - duplicate)
infrastructure_tips_1.md             infrastructure_tips_for_beginners.md
2026-02-03_Githubドキュメント...     github_docs_reading.md
```

#### Directories
- `articles/` - Polished, publishable content
- `guides/` - How-to documents and methodologies
- `app_ideas/` - Project specifications
- `prompts/` - Reusable prompt templates
- `interviews/` - Technical consultation records
- `notes/` - Quick references and troubleshooting

---

### "学習アウトプット" (No Changes to Existing Rules)
- Continue following AGENTS.md and CLAUDE.md
- Date format: `YYYY-MM-DD`
- Set management: 6-week cycles
- Skills remain unchanged

---

## 7. Cross-Reference Handling

### Finding: Zero Cross-References
Grep analysis found **no references** between:
- Learning logs ↔ General guides
- Daily reviews ↔ App ideas
- Agent skills ↔ Articles

**Implication**: Clean separation is possible with no link breakage.

---

### Future Cross-Referencing (If Needed)

#### Option A: Absolute Paths (Recommended)
```markdown
See also: [App Development Guide](file:///Users/310tea/Documents/アウトプット集/guides/app_development_guide.md)
```

#### Option B: Relative Repository References
```markdown
See also: `アウトプット集/guides/app_development_guide.md`
```

#### Option C: GitHub Links (If Pushed)
```markdown
See also: [App Development Guide](https://github.com/user/outputs/blob/main/guides/app_development_guide.md)
```

---

## 8. Decision Criteria for Future Files

### File Placement Questionnaire

Ask these questions for any new file:

#### 1. Does it contain RUNTEQ-specific content?
- YES: Consider "学習アウトプット"
- NO: Consider "アウトプット集"

#### 2. Does it reference specific dates or learning periods?
- YES: "学習アウトプット"
- NO: "アウトプット集"

#### 3. Is it consumed by agent skills or analytics?
- YES: "学習アウトプット"
- NO: "アウトプット集"

#### 4. Is it reusable across projects/contexts?
- YES: "アウトプット集"
- NO: "学習アウトプット"

#### 5. Does it contain metrics (Deep Score, etc.)?
- YES: "学習アウトプット"
- NO: "アウトプット集"

---

### Edge Case Examples

| File | Decision | Rationale |
|------|----------|-----------|
| RUNTEQ-specific mini-app reflection | "学習アウトプット" technical_interviews/ | References learning period, curriculum |
| General app development guide | "アウトプット集" guides/ | Reusable, no specific context |
| Debugging methodology | "アウトプット集" guides/ | General skill, not RUNTEQ-specific |
| Agent skill design memo | "学習アウトプット" notes/ideas/ | Part of learning system infrastructure |
| Rails troubleshooting note | "アウトプット集" notes/rails/ | General technical knowledge |

---

## 9. Rollback Plan

If separation causes issues:

### Immediate Rollback (Within 24 hours)
```bash
cd ~/Documents/学習アウトプット
git reset --hard HEAD~1  # Undo cleanup commit
```

Files remain in "アウトプット集" - no harm done.

---

### Selective Restoration (After 24 hours)
```bash
cd ~/Documents/アウトプット集
# Copy specific file back
cp guides/app_development_guide.md ~/Documents/学習アウトプット/docs/

cd ~/Documents/学習アウトプット
git add docs/app_development_guide.md
git commit -m "Restore: app_development_guide.md"
```

---

### Full Merge (Nuclear option)
```bash
cd ~/Documents/学習アウトプット
# Copy everything back
cp -r ~/Documents/アウトプット集/* ./

git add -A
git commit -m "Revert: Merge outputs back into main repository"
```

---

## 10. Testing & Validation

### Pre-Migration Checklist
- [ ] All files tracked in git (no uncommitted changes)
- [ ] Backup of entire repository (Time Machine or zip)
- [ ] Grep analysis confirms zero cross-references

### Post-Migration Validation
- [ ] All 23 files present in new repository
- [ ] Old repository has 23 fewer files
- [ ] Agent skills still functional (test format_daily_log)
- [ ] No broken links in README.md, AGENTS.md
- [ ] Git history preserved for critical files

### Functional Tests
```bash
# Test agent skill
cd ~/Documents/学習アウトプット
# Run format_daily_log skill - should work unchanged

# Test file access
ls daily/daily_2026-02-15.md  # Should exist
ls docs/daily_log_golden_rules.md  # Should exist
ls docs/app_development_guide.md  # Should NOT exist (moved)
```

---

## 11. Timeline & Effort Estimate

### Day 1 (2-3 hours)
- Create new repository structure
- Write README.md and .gitignore
- Copy first batch of files (articles, app ideas)
- Initial commit

### Day 2 (2-3 hours)
- Copy remaining files (guides, prompts, interviews, notes)
- Remove migrated files from old repository
- Update documentation (README, AGENTS.md)
- Final commits to both repositories

### Day 3 (1 hour)
- Validation testing
- Documentation review
- Announce to stakeholders (if applicable)

**Total Effort**: 5-7 hours spread over 3 days

---

## 12. Success Metrics

### Immediate (Post-Migration)
- [ ] Zero git errors or broken commits
- [ ] All 23 files successfully migrated
- [ ] Agent skills pass basic tests
- [ ] Documentation updated and accurate

### Short-term (1-2 weeks)
- [ ] User can find files faster (subjective)
- [ ] No confusion about file placement
- [ ] Git history remains clean and relevant

### Long-term (1-3 months)
- [ ] New files placed in correct repository instinctively
- [ ] Cross-contamination rate < 5%
- [ ] Maintenance time reduced (fewer irrelevant commits)

---

## 13. Additional Recommendations

### Consider Adding to "アウトプット集"

#### Topics to Expand
- Testing methodologies (RSpec, Capybara)
- Performance optimization guides
- Security best practices
- Code review checklists
- Architecture pattern references

#### Structure Enhancements
- Add `templates/` directory for reusable boilerplates
- Add `checklists/` for pre-deployment, security audits
- Add `references/` for quick lookups (Git commands, SQL cheatsheets)

---

### Consider Adding to "学習アウトプット"

#### Enhancements
- Cohort comparison reports (anonymized)
- Quarterly retrospectives (every 12 weeks)
- Skill progression tracking
- Mentor feedback integration

---

## 14. Risk Assessment

### Low Risk
- File copying (non-destructive)
- Creating new repository (isolated)
- Documentation updates

### Medium Risk
- Removing files from old repository (can be restored via git)
- Renaming files during migration (may confuse future searches)

### High Risk
- None identified (no code changes, no external dependencies)

### Mitigation
- Take full backup before starting
- Commit frequently (small, atomic changes)
- Test agent skills after cleanup
- Keep both repositories for 1 month before archiving old content

---

## 15. Conclusion

This separation strategy provides:

1. **Clear Boundaries**: RUNTEQ learning tracking vs. general web dev knowledge
2. **Safe Migration**: Copy-first approach with easy rollback
3. **Preserved History**: Git log for important files maintained
4. **Future-Proof**: Clear decision criteria for new files
5. **Low Risk**: No code changes, no external dependencies

**Recommendation**: Proceed with migration during low-activity period (weekend) to minimize disruption.

---

## Critical Files for Implementation

These files are most critical for executing this separation:

1. **/Users/310tea/Documents/学習アウトプット/README.md**
   - Reason: Must be updated to reflect focused scope after migration

2. **/Users/310tea/Documents/学習アウトプット/AGENTS.md**
   - Reason: Contains file placement rules that need updating

3. **/Users/310tea/Documents/学習アウトプット/.gitignore**
   - Reason: Template for new repository's .gitignore

4. **/Users/310tea/Documents/学習アウトプット/記事.md**
   - Reason: First article to migrate - sets pattern for others

5. **/Users/310tea/Documents/学習アウトプット/docs/app_development_guide.md**
   - Reason: Largest general guide - tests migration process for complex files
