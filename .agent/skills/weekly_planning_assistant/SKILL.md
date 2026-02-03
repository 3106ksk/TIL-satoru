---
description: Analyze weekly strategy input, generate JSON/Risk data, and update the Weekly Review file with checkpoints.
---

# Weekly Planning Assistant Skill

This skill automates the "Weekly Strategy Planning" process. It acts as an **Agile Learning Coach** to analyze your input, generate structured data, and update your weekly review document.

## 1. Input Analysis & Generation
1.  **Read Input**: Read the file containing the "Weekly Strategy Design" (or similar intent).
2.  **Analyze**: Act as a "Skilled Agile Learning Coach". Analyze the theme, capacity, experiments, and risks.
3.  **Generate Advice**: (Internal or temporary) Formulate strategic advice.
4.  **Create Files**:
    -   **Weekly Strategy Context (JSON)**:
        -   Path: `/Users/310tea/Documents/学習アウトプット/weekly_strategies/YYYY-MM-DD.json`
        -   Content: `theme`, `target_hours`, `experiment` (action, success_definition), `risks`, `success_criteria`.
    -   **Risk Assessment (Markdown)**:
        -   Path: `/Users/310tea/Documents/学習アウトプット/risk_assessments/YYYY-MM-DD.md`
        -   Content: List of risks and specific "If-Then" plans for each.

## 2. Checkpoint 1: Verify Generated Data
**CRITICAL**: You must pause here.
-   Call `notify_user` with the paths of the created files.
-   Message: "I have generated the Weekly Strategy JSON and Risk Assessment Markdown. Please check if the content is correct."
-   **WAIT** for user confirmation before proceeding.

## 3. Update Weekly Review File
1.  **Identify Target File**: specific markdown file (e.g., `2026-01-26_to_02-01.md`). If not specified, ask or infer from the date.
2.  **Update "This Week's Goals"**:
    -   Locate the section: `##### 【今週の目標】（行うこと、意識して取り組むことを具体的に）`.
    -   **Replace** the content with a synthesized summary of the strategy:
        -   Theme & Targets
        -   **Focus Experiment (The One Thing)**: Action & Success Definition.
        -   **Risk Mitigation (If-Then)**: Bullet points of the key protections.
        -   **Engineer Mindset**: Key mindset for the week.

## 4. Checkpoint 2: Verify File Update
**CRITICAL**: You must pause here.
-   Call `notify_user` with the path of the updated weekly review file.
-   Message: "I have updated the 'This Week's Goals' section in [filename]. Please check if the reflection matches your intent."
-   **WAIT** for user confirmation.

## 5. Generate Community Report
1.  **Extract Content**: Extract the content for "Community Report" (e.g., from `##### 【他のRUNTEQ生に伝えたいこと・意気込みなど！】` or similar).
2.  **Create File**:
    -   Path: `/Users/310tea/Documents/学習アウトプット/community_reports/YYYY-MM-DD_report.md`
    -   Content: The extracted text.
3.  **Clean Up**: **Remove** the extracted section from the Weekly Review File to avoid duplication.
4.  **Checkpoint 3**: Notify the user.
    -   Message: "I have extracted the community report to [new path] and removed it from the review file."

## Usage
Run this skill when you have drafted your "Weekly Strategy Design" and want to solidify the plan.
