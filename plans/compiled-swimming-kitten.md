# Daily Review 整形プロセスの構築

## Context

現在、Notionエクスポートの生データから `daily/daily_YYYY-MM-DD.md` への変換プロセスが自動化されておらず、手動またはアドホックなAI指示で行われている。また、既存の `normalize.py` の `parse_daily_markdown()` が期待するセクションヘッダーと実際のdailyファイルのフォーマットが不一致。

memo.md の仕様に基づき、新しいdailyフォーマットを定義し、2026-02-10の生データを整形する。

### 決定事項
- **Top1/Done条件 & 時間配分フィードバック**: AIがセッションデータ+生データから分析生成
- **セッション一覧テーブル**: dailyファイルには含めない（Stats算出の裏データとしてのみ使用）

## Step 1: `daily/daily_2026-02-10.md` の作成

### 入力
- Daily生データ: `notion_exports/ExportBlock-8b052950-.../2026-02-10 ...319.md`
- Sessions CSV: `notion_exports/ExportBlock-0619e91d-.../Sessions/Sessions DB(...).csv`（2026-02-10のレコードのみ抽出）

### セッションデータからの算出（AI処理）
Sessions CSVの2026-02-10レコード12件を分類:
- **Study**: 🧠計画・振り返り(18+30min) + 👨‍💻カリキュラム(37+27+70+23+52min) = **257 min**
- **Rest**: 69+14+80+30 = **193 min**
- **Exercise**: 77 = **77 min**
- Budget達成率: 257/300 = **85.7%**

### 出力フォーマット

`daily/daily_2026-02-10.md` を以下の構成で作成:

```
# 2026-02-10

## ■ Stats
- **Day Mode**: OFF（学習日）
- **Budget**: 300 min
- **Total Min**: 527 min
- **純粋な学習時間**: 257 min
- **休憩時間**: 193 min
- **運動時間**: 77 min
- **Avg Deep Score**: 2.9
- **Top1**: パスワードリセット完了
- **Done条件**: includesについて再度学習して技術面談にて相談

## ■ Top1 / Done条件 達成度フィードバック
（AIがセッションnotes + 生データのContext&Reflectionから定量・定性分析を生成）

## ■ 時間配分フィードバック
（AIがセッション時系列データ + Budget値から定量・定性分析を生成）

## ■ Worked
（Fact + Why形式に整形。下記ルール参照）

## ■ Slipped
（Fact + Why形式に整形。下記ルール参照）

## ■ Insights
（Fact + Why形式に整形。下記ルール参照）

## ■ Study Strategy for Next Day
（生データの ### 💡 Study Strategy for Next Day セクションをそのまま転記）

## ■ Technical Learnings
（生データの ## 📝 Context & Reflection 内のQ&A・コードブロックを構造化して転記）
```

### Worked / Slipped / Insights 整形ルール（Fact + Why形式）

1. 各項目は必ず `**Fact**` + `**Why**` の2行構成
2. **Fact** = セッションデータ・notesから裏取りできる客観的事実のみ（数値があれば含める）
3. **Why** = Factの原因・メカニズム（生データの記述 + セッションログからのAI推論）
4. Workedが空/プレースホルダーの場合、AIがセッションnotesから良かった行動を抽出して生成
5. 1セクション最大3項目（週次分析で扱いやすい量に制限）

**整形の入力ソース:**
- セッションCSVの当日レコード（notes, Deep Score, duration, Type）
- 生データの Context & Reflection
- 生データの Worked / Slipped / Insights の記述

## Step 2: `normalize.py` の `parse_daily_markdown()` を新フォーマット対応に更新

**対象ファイル**: `.agent/skills/normalize_learning_log/scripts/normalize.py` (L78-133)

変更内容:
- セクションヘッダー検出を新旧両方に対応:
  - `### Worked` / `## ■ Worked` → `"worked"`
  - `### Slipped` / `## ■ Slipped` → `"slipped"`
  - `### Insight` / `## ■ Insight` → `"insight"`
- 新セクション追加: `## ■ Strategy for Next Day` → `"strategy_for_next_day"`
- `Day Mode` 検出パターンはそのまま維持

## Step 3: `analysis_prompt_v2.md` の更新

**対象ファイル**: `prompts/analysis_prompt_v2.md`

変更内容:
- `days` 内の `reflection` に `strategy_for_next_day` フィールド追加を反映
- dailyファイルに含まれるTop1/Done条件フィードバック・時間配分フィードバックの情報を週次分析でも活用するよう指示を追記

## 検証方法

1. `daily/daily_2026-02-10.md` の内容が生データ+セッションデータの全情報を網羅しているか目視確認
2. `normalize.py` を実行し、新フォーマットのdailyファイルが正しくパースされるか確認
3. 既存の古いフォーマットのdailyファイル（旧`**Worked**`形式）も引き続きパース可能か確認（後方互換性）
