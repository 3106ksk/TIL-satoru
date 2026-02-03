---
name: daily_log_qc
description: Audit a Daily Review markdown file for Golden Rules compliance and suggest or apply fixes.
---

# Daily Log Quality Checker Skill

Use this skill when the user asks to validate, lint, or improve a Daily Review for AI analysis quality.

## References
- `docs/daily_log_golden_rules.md` (load when you need rule details)

## Workflow

1. **Open the target file** and confirm it is a Daily Review.
2. **Structure check**:
   - H1 title: `# YYYY-MM-DD Daily Review`
   - H2 order: Stats → Context & Reflection → Technical Learnings
   - H3 sections: Worked / Slipped / Insight
3. **Normalization check** (see Golden Rules for exact constraints):
   - Date format ISO, Day Mode allowed values (Off (OFF) / Shift (ON))
   - Total Min integer with `min`
   - Deep Score numeric
   - Top1 single line
4. **Noise check**:
   - Notion links (`Untitled`), relation lists, or metadata fields removed
5. **Duplication check**:
   - Stats values are not restated in other sections
   - Worked/Slipped/Insight do not repeat the same sentence
   - Technical Learnings are unique topics

## Output
- If issues exist, list them with short fix suggestions and line references.
- If clean, explicitly state "No issues found".
- If the user asks to fix, apply safe edits (headings, label normalization, metadata removal, section order).
