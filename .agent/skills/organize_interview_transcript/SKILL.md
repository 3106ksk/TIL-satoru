---
name: organize_interview_transcript
description: Renames and moves technical interview transcript files based on their content and creation date.
---

# Organize Interview Transcript

This skill automates the organization of technical interview transcripts.

## 1. Get File Information
- **Input**: You will be provided with a target file path (or multiple paths).
- **Action**:
    - For each file:
        - Run `stat -f "%SB" <filepath>` (on Mac) to get the Creation Date.
        - Read the file content to understand the topic.

## 2. Determine Filename
- **Date**: Use the file creation date found in step 1 (Format: `YYYY-MM-DD`).
    - *Note*: If the content explicitly states the interview date, verify if that is preferred. Default to creation date as per user preference "日付は可能であればファイルが作成された日を".
- **Title**: Summarize the *main topic* of the interview from the content into a short, descriptive title (e.g., `Githubドキュメント読み解き`, `デバッグ手順`, `アプリ企画相談`).
    - Keep it concise.
    - Avoid spaces in the title part if possible, or use underscores.
- **Format**: `<YYYY-MM-DD>_<Title>.<original_extension>`
    - *Important*: Preserve the original file extension (e.g., `.md`, `.txt`). Do not convert to `.txt` unless the original was `.txt`.

## 3. Rename and Move
- **Destination**: `/Users/310tea/Documents/学習アウトプット/technical_interviews/transcripts/`
- **Cmd**: `mv "<original_path>" "<destination>/<new_filename>"`

## 4. Verification
- Confirm the file exists in the new location.
- Report the Move operation to the user (e.g., "Moved `file.txt` to `transcripts/2026-01-01_Title.txt`").
