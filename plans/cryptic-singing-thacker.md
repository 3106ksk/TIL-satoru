# Notion入力スキーマ最適化計画

## Context

現在のNotionデータ入力構造には、パイプラインで使用されていないフィールド、毎日コピペされる静的テンプレート、空欄のまま放置されるセクションが混在している。入力負担を軽減しつつ、処理パイプライン（extract_daily_sessions → format_daily_log → normalize_learning_log）に必要なデータを保持する再設計を行う。

**本計画は 2026-03-08 のNotionエクスポート実データに基づき確定済み。**

---

## 現状分析：入力負担の内訳

### Sessions DB（セッションごとの手動入力 = 7フィールド）
| フィールド | 入力方法 | パイプライン利用 |
|---|---|---|
| start time | 手動/タイマー | **使用** (時系列表示、duration算出) |
| end time | 手動/タイマー | **使用** |
| Type | ドロップダウン | **使用** (カテゴリ分類) |
| Notes | 自由記述 (やった/詰まった/気づいた/次) | **使用** (Worked/Slipped/Insights生成の核心データ) |
| Cognitive Headroom | 1-5 選択 | **使用** (Deep Score算出、sessions table表示) |
| Focus | 1-5 選択 | **使用** (Deep Score算出、sessions table表示) |
| Friction | 1-5 選択 | **使用** (Deep Score算出、sessions table表示) |

### Daily Review Page（1日1回の入力）
| フィールド/セクション | 入力方法 | パイプライン利用 |
|---|---|---|
| Budget（min） | 数値入力 | **使用** (達成率算出) |
| Day Mode | ドロップダウン | **使用** (format_daily_logの出力) |
| Satisfaction | 1-5 選択 | 参照用（パイプライン未使用、将来の分析用に保持） |
| Worked | 自由記述（しばしば空欄） | 補助的（空欄時はAIがsession notesから生成） |
| Slipped | 自由記述（しばしば空欄） | 補助的 |
| Insights | 自由記述（簡潔なメモ） | 補助的 |
| Study Strategy for Next Day | 自由記述 | 転記のみ |

---

## 削除・不要項目リスト

### A. Sessions DB — 削除すべきカラム（2項目）

| カラム名 | 削除理由 |
|---|---|
| **Status** | 全レコード "Done"。パイプラインでフィルタリングに使用されていない |
| **content** | 全レコード空欄。どのスクリプトからも参照なし |

※ Prep Min / Interview Min / WrapUp Min / TI Min は削除済み（現在のCSVに存在しない）

### B. Sessions DB — 自動計算・システム管理のまま保持（変更不要）

| カラム名 | 種別 | 説明 |
|---|---|---|
| Deep Score | formula | `(CH + Focus + (6 - Friction)) / 3`（小数第1位に丸め） |
| Deep Flag | formula | Deep Score閾値判定 |
| Deep Work Min | formula | 自動計算。Notion上の表示用 |
| duration (m)f | formula | start/end timeから自動算出 |
| Date | formula | 日付 |
| WeekKey | formula | 週番号 |
| In Last Week / In This Week | formula | 週判定 |
| Daily Review | relation | Notion内部リンク |
| 作成日時 | auto | Notionシステム自動付与 |
| #DeepScore | formula | Deep Scoreと同値。レガシー列の可能性あり、削除検討可 |

### C. Daily Review Page — 削除済みセクション

| セクション | 削除理由 |
|---|---|
| **入力プロトコル（全文）** | 毎ページに同一の静的テンプレートがコピペされていた。Notionのデータベース説明文に移動済み |

---

## 確定スキーマ（2026-03-08 実データ準拠）

### 1. Sessions DB — 確定スキーマ

**CSVエクスポート時のカラム構成（20列）:**

```
Status, Daily Review, WeekKey, Date, duration (m)f, start time, end time,
Type, Notes, Deep Score, Deep Flag, Deep Work Min, 作成日時,
In This Week, In Last Week, content, #DeepScore, CH, Focus, Friction
```

**手動入力（セッションごと）: 7フィールド**

| フィールド | 必須 | 説明 |
|---|---|---|
| start time | Yes | セッション開始 |
| end time | Yes | セッション終了 |
| Type | Yes | セッション種別（ドロップダウン） |
| Notes | Yes | やった/詰まった・気づいた/次 |
| Cognitive Headroom | Yes | 自己評価 1-5 |
| Focus | Yes | 自己評価 1-5 |
| Friction | Yes | 自己評価 1-5 |

**CH/Focus/Friction → 維持（確定）**

3指標を維持する。理由:
- 定性面・定量面の詳細分析に3指標が不可欠。単一指標では「なぜパフォーマンスが低下したか」の診断粒度が不足する
- CH（認知余裕）、Focus（集中度）、Friction（摩擦）はそれぞれ異なる軸の情報を提供し、組み合わせて初めて学習状態の多面的な把握が可能になる
- Deep Score formula: `round(((CH + Focus + (6 - Friction)) / 3) * 10) / 10`

**自動計算（変更なし）:**
- Date, duration (m)f, Deep Score, Deep Flag, Deep Work Min, WeekKey, In Last Week, In This Week, 作成日時 — 既存formula/auto維持

**削除対象:**
- Status, content（前述の通り）

### 1.5. Implementation Log — 別DBで最小管理

`読んだ` と `実装した` は別イベントであり、翌日以降に実装した場合に Sessions DB の過去レコードを探して更新する運用は負担が大きい。したがって、Implementation の記録は Sessions DB ではなく**別DB**で管理する。

**方針:**
- Sessions DB は「何を読んだか」の事実ログに限定する
- 実装で試した時だけ `Implementation Log` に新規1レコードを追加する
- relation は張らず、最小構成で開始する

**Implementation Log（最小構成）:**

| フィールド | 入力方法 | 説明 |
|---|---|---|
| Date | 日付 | 実装を試した日 |
| Topic | テキスト | 何を実装・検証したか |
| Source | テキスト | 参照元（例: Rails Guide validation） |
| Result | Select | 成功 / 部分成功 / 失敗 / 保留 |
| Learning | テキスト | 実装して分かったこと |
| Evidence | 任意 | URL / PR / ファイル名など |

**運用ルール:**
- 読書時: Sessions DB にのみ記録
- 実装時: Implementation Log にのみ記録
- 過去の読書セッションを遡って更新しない

### 2. Daily Review Page — 確定構造

**Properties（メタデータ）— 実データ準拠:**

| プロパティ | 種別 | 説明 |
|---|---|---|
| Date | 自動 | ページ日付 |
| Day Mode | 手動 (Select) | OFF：学習日 / Shift |
| Budget（min） | 手動 (Number) | 1日の学習予算 |
| Satisfaction | 手動 (Number) | 1日の満足度 1-5 |
| Total Min | rollup | セッション合計時間 |
| Deep Work Min | rollup | Deep Work時間合計 |
| Avg Deep Score | rollup | 学習セッション平均Deep Score |
| Sessions DB(参照先) | relation | セッションリンク |
| In Last Week | formula | 先週判定 |
| In This Week | formula | 今週判定 |
| WeekKey | formula | 週番号 |

**ページコンテンツ（実データ構造）:**

```
## 📝 Context & Reflection

### ✅ Worked：（うまくいったこと。箇条書き1-3行）

---

### 🚧 Slipped：（うまくいかなかったこと。箇条書き1-3行）

---

### 💡 Insights：（学習パターンの発見、メタ認知的気づき）

---

### 💡 Study Strategy for Next Day：（翌日のTop1候補や方針）

---

## ▫️📚Technical Learnings（技術学習があった日のみ記入）

### 1.
- Q：
- A：
- References：

---

### 2.
- Q：
- A：
- References：

---

## 🛠️ アプリ開発ログ（開発日のみ記入）

**アプリ開発{N}日目**

## **やったこと**

## **詰まったこと**

**Technical LearningsQ**:
**A**:

## 学んだこと
```

**変更点:**

1. **Worked / Slipped / Insights — 3セクション構造を維持**
   - 構造化された入力は2つの機能を持つ: (a) 書く側の思考整理の足場、(b) AIの分析・生成品質の安定化
   - セクションが空欄の場合、AIがsession notesからFact+Why形式で自動生成する既存フローは維持
   - ラベル・emoji表記は現行Notionテンプレートのまま変更なし

2. **入力プロトコル → 削除済み**
   - Notionのデータベース説明文に移動済み

3. **Satisfaction → 新規追加**
   - Daily ReviewプロパティにSatisfaction (1-5) を追加。1日の主観的満足度を記録
   - 現時点ではパイプライン未使用だが、将来の週次分析で活用可能

4. **▫️📚Technical Learnings — 独立セクションとして維持**
   - `## ▫️📚Technical Learnings（技術学習があった日のみ記入）` として独立見出し（`##`レベル）で配置。markdownコードブロックでは囲まない
   - 非開発日の技術学習、読書由来のQ&A、エラー調査の知見も daily/*.md に残す必要があるため、`🛠️ アプリ開発ログ` とは分離して保持する
   - 各エントリは `### N.` 見出し + `Q：` + `A：` + 任意 `References：` の構成。セクション間は `---` で区切る
   - format_daily_logのStep 4は、従来どおりこの独立セクションを primary source として daily 側へ転記する
   - **実装適用**: Daily Reviewには置かない。Implementation の事実は `Implementation Log` 別DBで管理し、二重入力を避ける

5. **🛠️ アプリ開発ログ — 新規追加**
   - 現在 `📝 Context & Reflection` 内に自由記述されていた「アプリ開発N日目」を**専用セクション化**
   - **dev_log生成のトリガー**: format_daily_logのStep 6が `## 🛠️ アプリ開発ログ` セクション（`##`レベル）+ `アプリ開発N日目` パターンで検出
   - **実データ構造**: 「アプリ開発{N}日目」→「やったこと」→「詰まったこと」→「Technical LearningsQ/A」→「学んだこと」の4ブロック構成。セッション単位のnotesとは異なり、その日の開発全体を俯瞰する粒度
   - 開発日以外はセクションごと省略

### 3. Notes構造の最適化

**現状:** やった / 詰まった・気づいた / 次（3-4セクション）

**提案:** 構造は維持するが、必須は「やった」のみ

```
やった: （必須）何をしたか
詰まった/気づいた: （任意）行き詰まりや発見があれば
次: （任意）次のセッションでやること
```

- 「やった」だけでもformat_daily_logは学習記録を生成可能
- 「詰まった」「気づいた」がある日はSlipped/Insightsの質が向上するが、必須にすると入力負担が増す
- 「次」は次セッション開始時の切り替えコスト削減に有効だが、入力が億劫な場合は省略可

---

## パイプラインへの影響

### 変更が必要なファイル

| ファイル | 変更内容 | 影響度 |
|---|---|---|
| [.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py](.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py) | **変更不要**。REQUIRED_COLUMNS（Deep Score, CH, Focus, Friction等）は全て実CSVに存在し、既存ロジックがそのまま動作する | なし |
| [.claude/skills/extract_daily_sessions/SKILL.md](.claude/skills/extract_daily_sessions/SKILL.md) | **変更不要**。出力フォーマット（Summary + Sessions table + Notes）は実データと整合 | なし |
| [.claude/skills/format_daily_log/SKILL.md](.claude/skills/format_daily_log/SKILL.md) | **要更新**。(1) Step 1: Satisfaction プロパティの読み取り追加 (2) Step 4: `## ▫️📚Technical Learnings` 見出し（`##`レベル、コードブロック外）+ `### N.` / `Q：` / `A：` / `References：` 形式への対応 (3) Step 6: `## 🛠️ アプリ開発ログ`（`##`レベル）の4ブロック構造（やったこと / 詰まったこと / Technical LearningsQ&A / 学んだこと）に合わせたトリガー・抽出ロジック更新 | **中** |
| [.claude/skills/normalize_learning_log/scripts/normalize.py](.claude/skills/normalize_learning_log/scripts/normalize.py) | 変更不要。入力はdaily/*.md（最終出力）であり、Notionスキーマの変更は直接影響しない | なし |

### 変更不要なもの
- normalize.pyの入力はdaily/*.md（最終出力）であり、Notionスキーマの変更は直接影響しない
- daily/*.mdの基本出力フォーマット（Stats, Worked, Slipped, Insights, 学習記録）は変更なし
- extract_daily_sessions.py のREQUIRED_COLUMNSは実CSVカラム構成と完全一致

---

## Before / After まとめ

### Sessions DB
| | Before（旧計画時） | After（実データ確定） |
|---|---|---|
| 手動入力/セッション | 7フィールド | **7フィールド**（CH/Focus/Friction維持） |
| CSVカラム数 | 20 | 20（Status, content は削除候補だが未削除） |
| 削除対象カラム | — | Status, content（2カラム） |
| 自動計算カラム | — | Deep Score, Deep Flag, Deep Work Min, duration (m)f, Date, WeekKey, In Last/This Week, 作成日時, #DeepScore |

### Implementation Log DB
| | Before | After |
|---|---|---|
| 実装適用の記録先 | なし / Sessions DBでの管理を検討 | **Implementation Log 別DB** |
| 入力単位 | — | 実装した時だけ1レコード追加 |
| relation | — | なし（最小構成） |

### Daily Review Page
| | Before | After（実データ確定） |
|---|---|---|
| Properties | Date, Budget, Sessions DB | Date, Day Mode, Budget, Satisfaction, Total Min, Deep Work Min, Avg Deep Score, Sessions DB(参照先), In Last/This Week, WeekKey |
| 入力セクション | Worked/Slipped/Insights/Strategy + 入力プロトコル | Worked/Slipped/Insights/Strategy + ▫️📚Technical Learnings + 🛠️アプリ開発ログ |
| 静的テンプレート | あり（入力プロトコル） | なし（削除済み） |
| Technical Learnings | 独立セクション（任意） | `## ▫️📚Technical Learnings` として独立セクション維持。コードブロック外、`### N.` + `Q：/A：/References：` 形式 |
| Satisfaction | なし | 追加（1-5） |
| Day Mode | なし | 追加（Select: OFF：学習日 / Shift） |

### 1日あたりの総入力量変化
- **Sessions DB**: CH/Focus/Friction維持（**セッションあたり手動入力7のまま**）。Status/contentは削除候補
- **Daily Review**: 入力プロトコル削除済み。Satisfaction (1-5) を新規追加。▫️📚Technical Learningsは独立セクション（コードブロック外）で `### N.` + `Q：/A：/References：` 形式で記入
- **Implementation**: 実装適用の事実は Sessions DB から分離し、必要時のみ Implementation Log に記録
- **正味の変化**: 常時記入セクションは4（Worked/Slipped/Insights/Strategy）+ Satisfaction。読書と実装を別イベントとして分けることで、過去セッションを遡って更新する負荷をなくす

---

## 確認事項（決定済み）

1. **CH/Focus/Friction → 維持** → **確定**。定性・定量分析に3指標が不可欠。Deep Scoreはformula `(CH + Focus + (6 - Friction)) / 3` で自動算出
2. **Day Modeプロパティ** → **実装済み**。Select: OFF：学習日 / Shift
3. **Satisfactionプロパティ** → **実装済み**。1-5の主観的満足度
4. **Daily Review構造**: Worked/Slipped/Insights/Strategyの4セクション構造を **現状維持** → 入力プロトコル削除済み
5. **▫️📚Technical Learnings**: `## ▫️📚Technical Learnings（技術学習があった日のみ記入）` として独立セクション維持（コードブロック外）。各エントリは `### N.` + `Q：` + `A：` + 任意 `References：` の構成
6. **🛠️ アプリ開発ログ**: `## 🛠️ アプリ開発ログ（開発日のみ記入）` としてdev_logトリガーを安定させる専用セクション。やったこと / 詰まったこと / Technical LearningsQ&A / 学んだことの4ブロック構成
7. **Avg Deep Score**: Notion側でrollup（リアルタイム表示用）、パイプライン側でCSV生データから独自算出（出力生成用）の二重構成を維持
8. **Verbalization Count**: 今回は維持。自動集計案は KPI定義変更を伴うため別提案として後続検討
9. **Implementation Log**: セクション1.5で設計済み（別DB、最小構成）。Reading SourceはSessions DBに追加せず、Implementation Logのみ別DBで管理する方針で確定

---

## 検証方法

1. 2026-03-08 のNotionエクスポート実データで extract_daily_sessions → format_daily_log の処理フローを実行
2. 出力されたdaily/*.mdが既存フォーマットと同等の品質であることを確認
3. 特に以下をチェック:
   - Stats値の正確性（Avg Deep ScoreがCH/Focus/Frictionから正しく算出されるか）
   - Satisfaction値が生データに存在することの確認（Stats出力への反映は将来検討）
   - Worked/Slipped/InsightsのFact+Why品質（構造化セクションからの読み取り + 空欄時のsession notes自動生成）
   - Technical Learningsの転記精度（`## ▫️📚Technical Learnings` セクションから `### N.` + `Q：/A：/References：` 形式で daily へ正しく転記されるか）
   - dev_log生成が `## 🛠️ アプリ開発ログ` + `アプリ開発N日目` パターンで正しくトリガーされるか
   - 🛠️内の4ブロック（やったこと / 詰まったこと / Technical LearningsQ&A / 学んだこと）が dev_log に正しく反映されるか
   - Implementation Log が「実装した時だけ記録する」最小運用で継続可能か
