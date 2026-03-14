---
name: format_daily_log
description: Notion生データ + Sessions CSVから、最新フォーマットのdailyログを生成する。Fact+Why形式、AI分析フィードバック付き。開発ログがある日は共有用の開発ログも同時生成。
---

# Daily Log Formatter Skill (v2)

Notion生データとSessions CSVを入力に、`daily/daily_YYYY-MM-DD.md` を最新フォーマットで生成する。

## 設計方針

- **plans/compiled-swimming-kitten.md** を正とするフォーマット定義
- Worked / Slipped / Insights は **Fact + Why形式** で整形（生データの丸写しはNG）
- Top1/Done条件フィードバック、時間配分フィードバックは **AI生成**

## 入力データ

1. **Daily生データ**: `notion_exports/ExportBlock-*/YYYY-MM-DD *.md`
2. **Sessions記録**: `daily_sessions_record/sessions_YYYY-MM-DD.md`（`extract_daily_sessions` スキルで事前生成済み）
   - 該当ファイルが存在しない場合のみ、`notion_exports/` 内のSessions CSVから直接抽出する
3. **Daily Plan**（補完用）: `daily_plan/daily_YYYY-MM-DD_plan.md`（Done条件・切れたら→が生データに記載されていない場合の補完ソース）

## 処理フロー

### Step 1: データ読み込みと集計

1. Daily生データからプロパティ抽出:
   - Date, Day Mode, Budget, Top1, Done条件, Total Min, Avg Deep Score
   - Done条件・切れたら→が生データに未記載の場合、Daily Planから補完
2. `daily_sessions_record/sessions_YYYY-MM-DD.md` からセッションデータを読み込み分類:
   - **Study**: 🧠計画・振り返り + 👨‍💻カリキュラム + 📚読書 + 🗣Interview
   - **Rest**: Rest タイプ
   - **Exercise**: Exercise タイプ
3. 算出:
   - 純粋な学習時間 = Study系セッションの合計duration
   - 休憩時間 = Restセッションの合計duration
   - 運動時間 = Exerciseセッションの合計duration
   - Budget達成率 = 純粋な学習時間 / Budget
   - **Avg Deep Score = Restセッションを除外した学習セッションの平均Deep Score**

### Step 2: AI分析セクション生成

**■ Top1 / Done条件 達成度フィードバック**
- `[定量面]`: Top1に関連するセッション数・時間、Done条件の達成有無を事実ベースで記述
- `[定性面]`: セッションnotesとContext & Reflectionから、Top1への到達度とDone条件の進捗を定性分析

**■ 時間配分フィードバック**
- `[定量面]`: Budget対比の達成率・差分、午前/午後/夜の時間帯別学習時間、非学習時間の内訳
- `[定性面]`: セッション時系列から学習リズム・休憩パターンの分析、Budget未達の主因特定

### Step 3: Worked / Slipped / Insights 整形（Fact + Why形式）

**整形ルール:**
1. 各項目は `**N. ラベル**` + `**Fact**` + `**Why**` の3行構成
2. **ラベル** = そのFact+Whyが何についてなのかを一言で表現（例: 「昼休憩後の即座再開」「メタ認知時間の不足」）
3. **Fact** = セッションデータ・notesから裏取りできる客観的事実のみ（数値があれば含める）
4. **Why** = Factの原因・メカニズム（生データの記述 + セッションログからのAI推論）
5. Workedが空/プレースホルダーの場合、AIがセッションnotesから良かった行動を抽出して生成
6. 1セクション最大3項目

**整形の入力ソース:**
- `daily_sessions_record/sessions_YYYY-MM-DD.md` のセッションデータ（notes, Deep Score, duration, Type）
- 生データの Context & Reflection
- 生データの Worked / Slipped / Insights の記述

### Step 4: Technical Learnings 転記

生データの `## 📝 Context & Reflection` 内にQ&A・コードブロックが存在する場合のみ転記する。

**原則: 元データの内容を忠実に保持する。AIによる要約・再構成・省略は行わない。**

**転記ルール:**
1. 各Q&Aの **見出し** のみ `**{N}. {領域}: {トピック}**` 形式に整形する
2. Q&Aの **本文**（説明文・具体例・コードブロック・テーブル）は **元データからそのまま転記**
3. 許可される編集は以下の3つのみ:
   - 誤字脱字の校正（例: `form_wtih` → `form_with`、`単数系` → `単数形`）
   - コードブロックへの言語指定追加（例: ` ``` ` → ` ```ruby `）
   - Notion特有のフォーマット崩れの修復（改行・インデント）
4. 元データの節構造（「〜とは」等の小見出し）、具体例（URLクエリ例、フォームPOST例等）、HTML全文、比較テーブルなどは **削除・要約してはならない**
5. 参照URLは末尾に `**Evidence**:` としてまとめる（元データに記載がある場合のみ）

**注意**: 生データにTechnical Learningsに該当する記載がない場合、このセクション自体を省略する

### Step 4.5: 切れたら→ 抽出

- 生データの `### 🔄 集中が切れたら→` セクション直下にある**太字テキスト**を抽出してStats の `切れたら→` フィールドに転記
- 当該セクションが存在しない場合のみ「（未設定）」と記載

### Step 5: ファイル出力

`daily/daily_YYYY-MM-DD.md` として以下の構成で出力:

```markdown
# YYYY-MM-DD

## ■ Stats
- **Day Mode**: {OFF（学習日） / Shift（ON）}
- **Budget**: {N} min
- **Total Min**: {N} min
- **純粋な学習時間**: {N} min
- **休憩時間**: {N} min
- **運動時間**: {N} min
- **Avg Deep Score**: {N}
- **Top1**: {テキスト}
- **Done条件**: {テキスト}
- **切れたら→**: {テキスト}

## ■ Top1 / Done条件 達成度フィードバック

**[定量面]**
- {AI生成}

**[定性面]**
- {AI生成}

## ■ 時間配分フィードバック

**[定量面]**
- {AI生成}

**[定性面]**
- {AI生成}

## ■ Worked

**1. {ラベル}**
- **Fact**: {客観的事実}
- **Why**: {原因・メカニズム}

## ■ Slipped

**1. {ラベル}**
- **Fact**: {客観的事実}
- **Why**: {原因・メカニズム}

## ■ Insights

**1. {ラベル}**
- **Fact**: {観察・気づき}
- **Why**: {背景・仮説}

## ■ 今日の学習記録

**今日やったこと**
- {セッション概要を narrative に記述。何に取り組んだか、流れで書く}

**詰まったこと**
- {行き詰まった具体的な箇所・問題を箇条書き}

**なぜそうなったか**
- {詰まった原因・根本的なメカニズムを説明}

**何を学んだか**
- {得られた知識・理解・気づきを箇条書き。他人が読んでも分かるレベルで}

## ■ Study Strategy for Next Day
- {生データからそのまま転記}

## ■ Technical Learnings

**1. {領域}: {トピック}**
- **Question**: ...
- **Answer**: ...
- **Code**:
  ```lang
  ...
  ```
```

### Step 6: 開発ログ生成

**フォーマット定義は `daily_reports/dev_log_format.md` を正とする。必ず参照してから生成すること。**

生データの `📝 Context & Reflection` または `🛠️ アプリ開発ログ` セクション内に、見出しまたは先頭行として `アプリ開発N日目`（Nは整数）が存在する場合のみ、共有用の開発ログを同時生成する。

**トリガー判定:**
- `アプリ開発N日目` パターンが存在する → Step 6 実行
- 存在しない → Step 6 スキップ
- `実装` / `開発` などの単一キーワード一致だけでは生成しない
- Step 6 スキップ時に同日 `daily_reports/dev_log_YYYY-MM-DD.md` が既に存在する場合は削除し、再実行結果と整合させる

**抽出対象（生データから）:**
1. **開発進捗**: 「アプリ開発N日目」で始まるブロック（実装内容のリスト含む）
2. **学習の気づき**: 実装プロセスに関するメタ認知的記述
3. **Technical Learnings**: **生データから直接転記**（Step 4の整形結果ではなく、元データを使用）

**原則: 開発ログのTechnical Learningsは、生データの `■ Technical Learnings` 以下の内容をそのまま転記する。AIによる要約・再構成は行わない。**

**出力フォーマット・構成ルール・転記時の編集基準は全て `daily_reports/dev_log_format.md` に従う。**

**出力先:** `daily_reports/dev_log_YYYY-MM-DD.md`

## 検証チェックリスト

出力後に以下を確認:
- [ ] Stats値がセッション記録（`daily_sessions_record/`）の集計と一致するか
- [ ] Fact行にセッションnotesからの裏取り根拠があるか
- [ ] Why行が推論であることが明確か（事実と混同していないか）
- [ ] 1セクション3項目以内か
- [ ] Technical Learningsの各Q&Aが個別トピックとして分離されているか
- [ ] **Technical Learningsの本文が元データから改変されていないか**（説明文・具体例・コードブロック・テーブルが省略・要約されていないこと）
- [ ] 開発ログ該当日の場合、`daily_reports/dev_log_YYYY-MM-DD.md` が生成されているか
- [ ] **開発ログのTechnical Learningsが生データから直接転記されているか**（daily側のStep 4整形結果ではなく、元データの構造を保持していること）
- [ ] 開発ログ非該当日の場合、`daily_reports/dev_log_YYYY-MM-DD.md` が生成されないこと（既存があれば削除されること）

## 参照ファイル

- `plans/compiled-swimming-kitten.md`: dailyログのフォーマット定義と整形ルールの正
- `daily_reports/dev_log_format.md`: **開発ログのフォーマット定義の正**（Step 6で必ず参照）
- `prompts/analysis_prompt_v2.md`: 週次分析プロンプト（このdailyが入力となる）
- `daily/daily_2026-02-10.md`: dailyログの実例（リファレンス実装）
- `daily_reports/dev_log_2026-03-13.md`: 開発ログの実例（リファレンス実装）
