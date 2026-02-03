---
name: process_sessions_db_export
description: Process a raw Notion Sessions DB export CSV: filter by date, convert to Markdown, rename, and cleanup.
---

# Process Sessions DB Export Skill

This skill automates the workflow of processing a raw CSV export from the Notion Sessions DB. It filters the data for a specific date range, converts it to a clean Markdown table, renames the file according to the naming convention, moves it to the correct directory, and helps with cleaning up the original file.

## Usage

1.  **Identify the Input CSV**: Locate the raw CSV file (usually in `notion_exports`).
2.  **Determine Date Range**: Identify the Start Date and End Date (YYYY-MM-DD) you want to extract (e.g., specific week).
3.  **Run the Python Script**: Execute the provided helper script.

## Instructions for Agent

1.  **Locate Input**:
    -   Find the raw CSV file path.
    -   Confirm it exists.

2.  **Execute Script**:
    -   Run the following command (adjusting paths and dates):
        ```bash
        python3 /Users/310tea/Documents/学習アウトプット/.agent/skills/process_sessions_db_export/scripts/process_sessions.py \
          "<input_csv_path>" \
          "YYYY-MM-DD" \
          "YYYY-MM-DD" \
          "/Users/310tea/Documents/学習アウトプット/Sessions"
        ```
    -   *Note*: The output directory is fixed to `/Users/310tea/Documents/学習アウトプット/Sessions` unless specified otherwise.

3.  **Verify Output**:
    -   Check if the script ran successfully and created the file `Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md` in the target directory.
    -   Report the result to the user.

4.  **Cleanup (Important)**:
    -   Once the new file is verified, **Delete** the original input CSV file from the `notion_exports` directory.
    -   If there are any other intermediate files created during the process (though the script handles most), delete them too.

## Prerequisites
-   Python 3 installed.
-   `markdown` conversion logic is handled by the script.

## Example
**User Request**: "Process the session export for last week (Jan 26-31)."

**Action**:
```bash
python3 /Users/310tea/Documents/学習アウトプット/.agent/skills/process_sessions_db_export/scripts/process_sessions.py \
  "/Users/310tea/Documents/学習アウトプット/notion_exports/Sessions DB Export.csv" \
  "2026-01-26" \
  "2026-01-31" \
  "/Users/310tea/Documents/学習アウトプット/Sessions"
```

**Follow-up**:
-   `rm "/Users/310tea/Documents/学習アウトプット/notion_exports/Sessions DB Export.csv"`
