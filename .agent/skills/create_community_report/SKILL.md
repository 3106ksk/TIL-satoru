---
description: Generate a weekly community report based on the weekly strategy JSON and risk assessment Markdown, following a specific format and tone.
---

# Create Community Report Skill

This skill automates the creation of a weekly "Community Report" markdown file. It consolidates data from your weekly strategy and risk assessment files into a structured report with a consistent tone and format.

## Prerequisities

Before running this skill, ensure you have:
1.  **Weekly Strategy JSON**: A file in `weekly_strategies/` covering the target week (e.g., `2026-02-09_to_2026-02-15.json`).
2.  **Risk Assessment Markdown**: A file in `risk_assessments/` for the target week (e.g., `2026-02-08.md`).

## Workflow

### 1. Identify Target Week & Files
1.  Determine the **Target Week** (usually the upcoming Monday-Sunday range).
2.  Locate the corresponding **Weekly Strategy JSON** (`weekly_strategies/YYYY-MM-DD_to_YYYY-MM-DD.json`).
3.  Locate the corresponding **Risk Assessment Markdown** (`risk_assessments/YYYY-MM-DD.md` or similar date).

### 2. Extract Data
1.  **From JSON**:
    -   `theme`: The main theme for the week.
    -   `target_hours`: Total study hours (e.g., "24.0").
    -   `experiment`:
        -   `action`: The specific action.
        -   `success_definition`: How success is measured.
    -   `risks`: (Optional, use Markdown if available for details).
2.  **From Markdown (Risk Assessment)**:
    -   Extract the **If-Then Plans**. Look for sections like `### 1. 対 「Risk Name」` and the corresponding `If` / `Then` content.
    -   Format them as: `・対 「Risk Name」：If... Then...` (condensed).

### 3. Generate Report Content
Create a new markdown file at `community_reports/YYYY-MM-DD_to_YYYY-MM-DD_report.md` with the following structure.

> **CRITICAL**: Use **Plain Form (Da/Ta style)** for all "Review" and "Mindset" sections. Do NOT use polite form (Desu/Masu).

#### Section 1: Last Week's Review (Placeholder)
*Since this data is not in the strategy files, generate a placeholder section for the user to fill in.*

```markdown
##### 【先週の振り返り】（行ったこと、意識したことを具体的に）
・学習した内容：
（ここに学習内容を箇条書きで記入）

・上手くいったこと：
【Good】 （〜できた。〜した。という常体で記入）

・できなかったこと：
【Bad】 （〜だった。〜してしまった。という常体で記入）

・学習時間/週： （ここに時間を記入）

＜エンジニアマインド振り返り＞
・実施したアクション：
（〜した。と記入）

・上手くいったこと/できなかったこと：
（〜だった。と記入）
```

#### Section 2: This Week's Goals (From JSON)
*Populate with data from the JSON.*

```markdown
##### 【今週の目標】（行うこと、意識して取り組むことを具体的に）
・学習する内容：{theme}
・目標学習時間：{target_hours}時間

**＜重点実験 (The One Thing)＞**
・行動：{experiment.action}
・成功定義：{experiment.success_definition}
```

#### Section 3: Risk Measures (From Markdown)
*Format the extracted If-Then plans.*

```markdown
**＜リスク対策 (If-Then)＞**
・対 「{Risk 1}」：{Condensed If-Then Plan}
・対 「{Risk 2}」：{Condensed If-Then Plan}
・対 「{Risk 3}」：{Condensed If-Then Plan}
```
*Note: Summarize the "Then" part to be concise.*

#### Section 4: Engineer Mindset Goals (Template)
*Generate the standard 4 items. If specific focus points are not in JSON, leave placeholders or infer from `theme`.*
*Use **Plain Form (Da/Ta style)**.*

```markdown
**＜エンジニアマインド目標＞**
1. 計画性 (Planning)
定義: 目標から逆算して、自らの行動を設計・調整する力
今週のフォーカス: 
・「{Infer focus from theme or leave blank}」
・{Infer action from target_hours/risks, e.g. "時間を厳しめに見積もる。"}

2. 論理的思考 (Logical Thinking)
定義: 物事の筋道や原因を整理し自分の考えを明確に伝えたり、次の行動に活かしたりする力
今週のフォーカス: 
・「{Infer focus, e.g. 言語化駆動の実装を継続する。}」

3. 素直さ (Honesty / Openness)
定義: 自分の課題やできていないことを認め、前向きに改善へつなげる力
今週のフォーカス: 
・「{Infer focus, e.g. 動画の誘惑には物理的遮断で対処する。}」

4. 自主性 (Initiative)
定義: 他人任せにせず、自分の意思と判断で行動する力
今週のフォーカス: 
・「{Infer focus, e.g. 一次情報にあたる姿勢を維持する。}」
```

### 4. Finalize
1.  **Save the file**.
2.  **Notify the user**: "I have created the draft community report at [path]. Please review and fill in the placeholders."

## Example Usage
"Create a community report for the week of Feb 9th."
-> The agent will look for `weekly_strategies/2026-02-09_to_2026-02-15.json` and generate the report.
