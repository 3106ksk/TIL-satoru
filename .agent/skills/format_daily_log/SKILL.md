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
   - **Auto-calculate** true work time by subtracting 'Rest' sessions (requires Sessions CSV).
   - Restructure the content into Stats, Context & Reflection, and Technical Learnings.

## References
- `docs/daily_log_golden_rules.md` (load when you need formatting or normalization details)

## Instructions for Agent

1. **Analyze the Input File**:
   - Read the current active file.
   - Identify the Date from the content (property like `Date`/`Time`, or in the title). If missing, ask the user or infer from filename.
   - Identify values for: `Day Mode`, `Total Min`, `Deep Score`, `Top1`.
   - Identify sections for: `Worked`, `Slipped`, `Insight`.
   - **Calculate Work Time**:
     - Look for a "Sessions" CSV file in `notion_exports` (e.g., `Sessions*.csv`).
     - If found:
       - Filter rows where `Date` matches the Daily Review date.
       - Identify "Rest" sessions (look for "Rest" in `Tag`, `Type`, or `Name` columns).
       - Sum the duration of these "Rest" sessions.
       - Subtract "Rest" duration from `Total Min`.
       - use this **Calculated Total Min** for the output.
   - Identify Technical Learnings content (body text/headers).
      - **CRITICAL**: Watch for multiple occurrences of "Q:" or "Question:". Each "Q:" should be treated as a SEPARATE topic in Technical Learnings. Do not merge them.
    - **Extract Research Stock**:
      - Look for the section `### 📥 Research Stock` or `### 未解決` (or similar).
      - If found:
        - Extract the list items/questions under it.
        - **Append** these items to `/Users/310tea/Documents/学習アウトプット/research_stock.md` under the `## 📥 Inbox` section.
        - **Exclude** this section and its content from the final Daily Log output.

2. **Construct new content** following this template:
   - **Important**: Use `■` for main sections (H2 equivalent) and `**Bold**` for subsections (H3 equivalent).
   - **Numbering**: Sequentially number the Technical Learning topics (e.g., **1. Domain: Topic**, **2. Domain: Topic**).

   ```markdown
   # {YYYY-MM-DD} Daily Review

   ■ Stats
   - **Day Mode**: {Value}
   - **Total Min**: {Calculated Total Min} min (Excluding Rest)
   - **Deep Score**: {Value}
   - **Top1**: {Value}

   ■ Context & Reflection
   **Worked**
   - 事実: {Content} / 理由: {Content}

   **Slipped**
   - 事実: {Content} / トリガー: {Content}

   **Insight**
   - 事実: {Content} / 次の一手: {Content}

   ■ Technical Learnings

   **1. {領域}: {具体的トピック}**
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
   - Ensure headings match the template above (using `■` and `**`).
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

■ Stats
- **Day Mode**: Off (OFF)
- **Total Min**: 187 min
...
```
