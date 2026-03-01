---
name: format_daily_log
description: Notion生データ + Sessions CSVから、最新フォーマットのDaily Reviewファイルを生成する。Fact+Why形式、AI分析フィードバック付き。
---

# Daily Log Formatter Skill (v2)

Notion生データとSessions CSVを入力に、`daily/daily_YYYY-MM-DD.md` を最新フォーマットで生成する。

## 設計方針

- **plans/compiled-swimming-kitten.md** を正とするフォーマット定義
- Worked / Slipped / Insights は **Fact + Why形式** で整形（生データの丸写しはNG）
- Top1/Done条件フィードバック、時間配分フィードバックは **AI生成**

## 入力データ

1. **Daily生データ**: `notion_exports/ExportBlock-*/YYYY-MM-DD *.md`
2. **Sessions CSV**: `notion_exports/ExportBlock-*/Sessions/Sessions DB*.csv`（対象日のレコードを抽出）

## 処理フロー

### Step 1: データ読み込みと集計

1. Daily生データからプロパティ抽出:
   - Date, Day Mode, Budget, Top1, Done条件, Total Min, Avg Deep Score
2. Sessions CSVから対象日のレコードを抽出し分類:
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
- セッションCSVの当日レコード（notes, Deep Score, duration, Type）
- 生データの Context & Reflection
- 生データの Worked / Slipped / Insights の記述

### Step 4: Technical Learnings 構造化

生データの `## 📝 Context & Reflection` 内にQ&A・コードブロックが存在する場合のみ、以下の形式で転記:

```
**{N}. {領域}: {トピック}**
- **Question**: {疑問}
- **Answer** / **Conclusion**: {回答・結論}
- **Evidence**: {参照URL等}（あれば）
- **Code**:
  ```lang
  コードブロック
  ```
```

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

## 検証チェックリスト

出力後に以下を確認:
- [ ] Stats値がセッションCSVの集計と一致するか
- [ ] Fact行にセッションnotesからの裏取り根拠があるか
- [ ] Why行が推論であることが明確か（事実と混同していないか）
- [ ] 1セクション3項目以内か
- [ ] Technical Learningsの各Q&Aが個別トピックとして分離されているか

## 参照ファイル

- `plans/compiled-swimming-kitten.md`: フォーマット定義と整形ルールの正
- `prompts/analysis_prompt_v2.md`: 週次分析プロンプト（このdailyが入力となる）
- `daily/daily_2026-02-10.md`: 最新フォーマットの実例（リファレンス実装）
