---
name: format_daily_log
description: Format a raw Notion export into the Daily Review Golden Structure and remove noise.
---

# Daily Log Formatter Skill

This skill takes a raw Notion markdown export of a daily log and reformats it according to the Golden Rules in `docs/daily_log_golden_rules.md`.

## Usage

1. **Open the raw markdown file** exported from Notion.
2. **Run this skill**.
3. The skill will:
   - Rename the file to `daily_YYYY-MM-DD.md`.
   - Clean up metadata and noise.
   - Restructure the content into Stats, Context & Reflection, and Technical Learnings.

## References
- `docs/daily_log_golden_rules.md` (load when you need formatting or normalization details)

## Instructions for Agent

1. **Analyze the Input File**:
   - Read the current active file.
   - Identify the Date from the content (property like `Date`/`Time`, or in the title). If missing, ask the user or infer from filename.
   - Identify values for: `Day Mode`, `Total Min`, `Deep Score`, `Top1`.
   - Identify sections for: `Worked`, `Slipped`, `Insight`.
   - Identify Technical Learnings content (body text/headers).
      - **CRITICAL**: Watch for multiple occurrences of "Q:" or "Question:". Each "Q:" should be treated as a SEPARATE `### {Topic}` section in Technical Learnings. Do not merge them.

2. **Construct new content** following this template:

   ```markdown
   # {YYYY-MM-DD} Daily Review

   ## Stats
   - **Day Mode**: {Value}
   - **Total Min**: {Value} min
   - **Deep Score**: {Value}
   - **Top1**: {Value}

   ## Context & Reflection
   ### Worked
   - 事実: {Content} / 理由: {Content}
   ### Slipped
   - 事実: {Content} / トリガー: {Content}
   ### Insight
   - 事実: {Content} / 次の一手: {Content}

   ## Technical Learnings
   ### {領域}: {具体的トピック}
   - **Issue** / **Question**: {Choose based on context: Trouble vs Generic Question}
   - **Cause**: {If known}
   - **Solution/Hypothesis** / **Conclusion**: {Resolution (if Issue) / Answer (if Question)}
   - **Evidence**: {If known}
   - **Code**:
     ```lang
     # Code block if present
     ```
   ```

3. **Apply Formatting Rules**:
   - **Remove** all other metadata lines (Created time, Tags, etc.).
   - **Remove** "Untitled" links and Notion relation link lists.
   - Ensure headings (H1/H2/H3) match the template above.
   - Preserve code blocks with correct language identifiers.
   - Follow `docs/daily_log_golden_rules.md` for normalization details (units, labels, ordering).

4. **Action**:
   - Create the new file `daily/daily_{YYYY-MM-DD}.md` with the constructed content.
   - Do NOT overwrite the original file yet.

5. **Verification & Cleanup**:
   - Notify the user that the new file has been created and request them to verify the content.
   - Explicitly ask: "Shall I delete the original file {OriginalFileName} now?"
   - If the user approves, delete the original file.

## Example Transformation

**Input (Snippet):**
```markdown
# 2026-01-27
Day Mode: 🏠 Off (OFF)
Total Min: 187
Created time: 2026-01-27 ...
```

**Output:**
```markdown
# 2026-01-27 Daily Review

## Stats
- **Day Mode**: Off (OFF)
- **Total Min**: 187 min
...
```
