# Daily Plan 入力テンプレート

> このテンプレートをコピーして記入し、「今日の学習計画を作成して」と指示する。
> スキル: `.claude/skills/generate_daily_plan/SKILL.md`

---

## A. ユーザー入力（必須3項目）

- **対象日付**: YYYY-MM-DD
- **Day Mode**: OFF / Shift（勤務時間: HH:MM-HH:MM）
- **学習可能時間**: （例: 6時間, 18時以降の90分, 8:00-12:00の4時間）

## B. 前日コンテキスト（任意・補足用）

> 以下は通常スキルが自動読込するが、該当ファイルがない場合はここに直接記入する。

### 前日の実績サマリ
- **前日の日付**: YYYY-MM-DD
- **Top1達成**: ✅ / ❌（内容: ）
- **学習時間**: — min（Budget — min）
- **Avg Deep Score**: —
- **持ち越しタスク**:
- **Worked**:
- **Slipped**:
- **Insight**:

### 認知リソース状態
- **バーンアウト兆候**: あり / なし
- **根拠**: （前日のBudget超過率、DS推移など）

## C. 自動参照ファイル（スキルが読み込む）

| ファイル | パス | 用途 |
|---|---|---|
| 週次戦略 | `weekly_strategies/weekly_strategy_{start}_to_{end}.md` | 週テーマ・daily_top1・リスク対策 |
| 前日のdaily review | `daily/daily_{前日日付}.md` | Worked/Slipped/Insight・Stats |
| 前日のdaily plan | `daily_plan/daily_{前日日付}_plan.md` | 達成状況・持ち越しタスク |
