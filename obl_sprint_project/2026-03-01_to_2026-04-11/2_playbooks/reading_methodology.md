# Reading Methodology - OBL Cycle 2 (2026-02-23 〜 2026-04-05)

**作成日**: 2026-02-23
**対象期間**: OBL Cycle 2（ミニアプリ完成＋デプロイ）
**目的**: 技術書の参照判断基準とKPI設計を明確化し、「読んだ→試した→言語化できた」の全フローを追跡する

---

## 前提

本ドキュメントは [Reading Trigger Design](reading_trigger_design.md) と対をなす。
- **Reading Trigger Design**: 「**いつ**読むか」（トリガー、タイミング、時間配分）
- **Reading Methodology**: 「**どう**読むか」（参照判断、読み方、KPI測定）

---

## 1. 技術書の種類別アプローチ - 状況ベース判断基準

### 基本原則

技術書の参照は「**状況**」を軸に判断する。「この状況なら→この種類を参照する/しない」という明確なif-thenルールに従う。

**技術書の種類**:
1. **公式ドキュメント**（Railsガイド、Ruby公式ドキュメント）
2. **gem/ライブラリのREADME**（GitHub、RubyGems）
3. **技術記事**（Qiita、Zenn、個人ブログ）
4. **技術書籍**（紙の本、電子書籍）
5. **Stack Overflow/GitHub Issues**（Q&Aサイト）

---

### 状況1: 新機能実装前（Off Day朝9:00-9:30）

**トリガー**: 「朝食後→即Reading」（30min）

#### 参照すべき

| 優先度 | 種類 | 理由 | 具体例 |
|---|---|---|---|
| **1** | **公式ドキュメント** | 信頼性最高、最新情報、体系的 | Railsガイド「Active Record の基礎」 |
| **2** | **gem/ライブラリのREADME** | 使い方の実例、設定方法が明確 | Ransack gemのREADME（検索機能実装時） |
| 3 | 技術記事（2024年以降） | 実装パターンの補足、ハマりポイント | Qiita「Ransackで検索機能を実装する」 |

#### 参照すべきでない

| 種類 | 理由 | 代替手段 |
|---|---|---|
| **古い技術記事**（2023年以前） | Rails/gemのバージョンが古い、非推奨な実装 | 公式ドキュメントで最新情報を確認 |
| **技術書籍の通読** | 30minでは読み切れない、実装に直結しない | 概念理解は週末の深い学習時間に回す |
| **Stack Overflow** | 問題が発生していない段階では不要 | エラー発生時に参照 |

#### 読み方

- **目的**: 今日の実装で使う「語彙」と「構造」をインプットする
- **アプローチ**: 目次ベース読み
  1. 目次を見て、今日の実装に関連する章を特定（5min以内）
  2. 該当章を通読（20min）
  3. コード例があれば流し読み（完全理解は不要、実装時に深まる）
- **ノート取り**: **しない**（まず語彙を浴びる、実装時に深まる）
- **理解度**: 60-70%でOK（完璧主義を避ける）

---

### 状況2: エラー発生時（30min自己解決フェーズ）

**トリガー**: 実装中にエラーが発生し、5min考えても解決しない

#### 参照すべき

| 優先度 | 種類 | 理由 | 具体例 |
|---|---|---|---|
| **1** | **公式ドキュメント** | エラーメッセージで検索、正確な原因特定 | Railsガイドで「NoMethodError」を検索 |
| **2** | **Stack Overflow/GitHub Issues** | 同じエラーの解決事例、具体的な修正コード | Stack Overflowで「ActiveRecord::RecordNotFound」検索 |
| **3** | **技術記事** | エラーの原因解説、ハマりポイント | Qiita「よくあるRailsエラーと対処法」 |
| 4 | gem/ライブラリのIssues | gemのバグ報告、バージョン固有の問題 | RansackのGitHub Issuesで「undefined method」検索 |

#### 参照すべきでない

| 種類 | 理由 | 代替手段 |
|---|---|---|
| **技術書籍** | エラー解決には時間がかかりすぎる | 30min自己解決後、技術面談で質問 |
| **動画チュートリアル** | 該当箇所を探すのに時間がかかる | 技術記事で素早く検索 |
| **ChatGPT/AI**（初手） | まず公式ドキュメントを見る習慣をつける | 公式を見ても分からなければAI活用 |

#### 読み方

- **目的**: エラーの原因を特定し、修正方法を見つける
- **アプローチ**: 検索駆動読み
  1. エラーメッセージをコピー（完全一致検索）
  2. 公式ドキュメントで検索（5min）
  3. 見つからなければStack Overflow、技術記事へ（15min）
  4. 解決策を試す（10min）
- **ノート取り**: **する**
  - エラーメッセージ、原因、解決策を Daily Review の「Fact + Why」に記録
  - 次回同じエラーが出た時のために語彙を残す
- **理解度**: 解決できればOK（深い理解は後回し）

---

### 状況3: 概念理解時（週末の深い学習時間）

**トリガー**: 週次レビュー後、次週の実装テーマを深く理解したい

#### 参照すべき

| 優先度 | 種類 | 理由 | 具体例 |
|---|---|---|---|
| **1** | **技術書籍** | 体系的、深い理解、背景知識 | 「現場で使えるRuby on Rails」 |
| **2** | **公式ドキュメント**（詳細章） | 内部実装、高度な機能 | Railsガイド「Active Record の高度な機能」 |
| **3** | **技術記事**（解説系） | 概念の図解、実装例との対比 | Zenn「Active Recordの仕組みを理解する」 |

#### 参照すべきでない

| 種類 | 理由 | 代替手段 |
|---|---|---|
| **gem/ライブラリのREADME** | 概念理解には不向き（使い方中心） | 公式ドキュメントの理論章を読む |
| **Stack Overflow** | 問題解決型、概念理解には不向き | 技術書籍で体系的に学ぶ |

#### 読み方

- **目的**: 「なぜそうなるのか」を理解し、次週の実装で応用できる状態にする
- **アプローチ**: 通読＋実装検証
  1. 技術書籍の該当章を通読（60-90min）
  2. 重要な概念をノートに記録
  3. 簡単なコードで動作確認（30min）
- **ノート取り**: **する**
  - 概念の定義、図解、コード例を記録
  - 次週の実装で参照するために整理
- **理解度**: 80-90%（実装で応用できるレベル）

---

### 状況4: 実装パターン探索時（実装中）

**トリガー**: 「どう書くのが良いか」が分からない（バリデーション、リファクタリング、UI設計など）

#### 参照すべき

| 優先度 | 種類 | 理由 | 具体例 |
|---|---|---|---|
| **1** | **gem/ライブラリのREADME** | 実装例が豊富、ベストプラクティス | Ransack README「Advanced Usage」 |
| **2** | **技術記事**（実装例） | 実際のプロジェクトでの使い方 | Qiita「Railsでよく使うバリデーション集」 |
| **3** | **GitHub実装例** | 他のプロジェクトのコード参照 | RUNTEQサンプルアプリのコード |

#### 参照すべきでない

| 種類 | 理由 | 代替手段 |
|---|---|---|
| **公式ドキュメント**（理論章） | パターン探索には時間がかかる | gem READMEの実装例を見る |
| **技術書籍** | パターン探索には不向き（体系的すぎる） | 技術記事で素早く実装例を検索 |

#### 読み方

- **目的**: 実装パターンを見つけ、コピペではなく理解して適用する
- **アプローチ**: コード中心読み
  1. gem READMEの実装例を流し読み（10min）
  2. 自分の実装に近い例を選ぶ（5min）
  3. コードを理解して、自分のコードに適用（15min）
- **ノート取り**: **軽く**
  - 使ったパターンを Daily Review の「Fact」に記録
  - 「なぜこのパターンを選んだか」をWhyに記録
- **理解度**: 70-80%（適用できればOK）

---

### 状況5: Shift Day帰宅後（15min予習）

**トリガー**: 帰宅後着替え後、翌日の実装テーマの予習

#### 参照すべき

| 優先度 | 種類 | 理由 | 具体例 |
|---|---|---|---|
| **1** | **公式ドキュメント**（目次のみ） | 翌日の実装の「地図」を手に入れる | Railsガイド「Active Record バリデーション」の目次 |
| **2** | **gem/ライブラリのREADME**（冒頭） | 翌日使うgemの概要を掴む | Ransack READMEの「Getting Started」 |

#### 参照すべきでない

| 種類 | 理由 | 代替手段 |
|---|---|---|
| **詳細章** | 15minでは読み切れない、Cognitive Headroom 2-3 | 翌日朝30minで詳細を読む |
| **技術記事** | 予習には不要（実装時に参照） | 公式ドキュメントの目次で十分 |
| **技術書籍** | 軽負荷Reading向きではない | 週末の深い学習時間に回す |

#### 読み方

- **目的**: 翌日の実装で「何をするか」の全体像を掴む
- **アプローチ**: 目次ベース読み（軽負荷）
  1. 公式ドキュメントの目次を眺める（5min）
  2. 翌日使いそうなセクションを特定（5min）
  3. 冒頭部分を流し読み（5min）
- **ノート取り**: **しない**（翌日朝に改めて読む）
- **理解度**: 30-40%でOK（予習レベル）

---

### 「参照しない」基準のまとめ

以下の場合、技術書の参照を**止める**：

| 状況 | 止める基準 | 理由 |
|---|---|---|
| **時間制約がある時** | 15min以上かかる深い本 | Cognitive Headroomが低い、実装時間を圧迫 |
| **実装パターンが必要な時** | 理論中心の公式ドキュメント | パターン探索には不向き |
| **公式ドキュメントがある時** | 古い技術記事（2023年以前） | 情報が古い、非推奨な実装 |
| **エラー解決時** | 技術書籍の通読 | 時間がかかりすぎる、30min自己解決ルールに反する |
| **朝30min Reading時** | ノート取り | まず語彙を浴びる、実装時に深まる |

---

## 2. KPI設計と測定方法

### 主KPI: Implementation Rate（実装活用率）

**定義**:
```
Implementation Rate = (読んだ内容を実装で試した日数) / (Reading実施日数) × 100%
```

**目標**: **80%以上**

**測定方法**:
1. **Daily Review記録時**（毎日18:00-18:15）
   - Reading実施日に「読んだ内容を試したか」をYes/Noで記録
   - Daily ReviewのFactに「〇〇について読んだ→実装で△△を試した」を明記

2. **週次レビュー集計時**（毎週日曜）
   - Yes日数をカウント
   - Implementation Rate = Yes日数 / Reading実施日数 × 100%

**記録例**:

```markdown
## Daily Review - 2026-02-24

### Fact
- 9:00-9:30: Railsガイド「Active Record マイグレーション」を読んだ（30min）
- 9:30-12:00: マイグレーションファイルを作成し、外部キー制約を追加した（読んだ内容を試した）
- **Implementation Flag**: Yes

### Why
- 外部キー制約（foreign_key: true）を使う理由は、データの整合性を保つため
- add_referenceメソッドで外部キー制約を自動生成できることを学んだ
```

**週次集計例**:

| 日付 | Reading実施 | Implementation Flag | 備考 |
|---|---|---|---|
| 2/23（日） | Yes | Yes | Railsガイド「関連付け」→ ER図作成 |
| 2/24（月） | Yes | Yes | Railsガイド「マイグレーション」→ 外部キー追加 |
| 2/25（火） | Yes | Yes | Railsガイド「基礎」→ モデル設計 |
| 2/26（水） | Yes（Shift Day 15min） | No | 予習のみ、翌日に試す予定 |
| 2/27（木） | Yes | Yes | 昨日読んだバリデーションを実装 |
| 2/28（金） | Yes（Shift Day 15min） | No | 予習のみ |
| 3/01（土） | Yes | Yes | CRUD実装開始 |

**Implementation Rate = 5 / 7 = 71.4%**（目標80%未達、PIVOT検討）

---

### 副KPI: Verbalization Score（言語化スコア）

**定義**:
```
Verbalization Score = Daily ReviewのWhyで技術用語を使った回数（週合計）
```

**目標**: **週20回以上**

**測定方法**:
1. **Daily Review記録時**（毎日18:00-18:15）
   - Whyセクションで技術用語を使う（意識的に語彙を使う）
   - 技術用語: Rails固有の概念、gem名、メソッド名、デザインパターンなど

2. **週次レビュー集計時**（毎週日曜）
   - 各日のDaily ReviewのWhyセクションで技術用語をカウント
   - 週合計を算出

**技術用語の例**:
- **Rails固有**: Active Record、マイグレーション、バリデーション、関連付け、コントローラ、ルーティング
- **メソッド名**: add_reference、belongs_to、has_many、validates、render、redirect_to
- **gem名**: Ransack、Kaminari、Devise
- **デザインパターン**: MVC、REST、CRUD

**記録例**:

```markdown
## Daily Review - 2026-02-24

### Why
- 外部キー制約（foreign_key: true）を使う理由は、データの整合性を保つため ← 技術用語1
- add_referenceメソッドで外部キー制約を自動生成できることを学んだ ← 技術用語2
- belongs_toとhas_manyの関連付けで、データベースの正規化を実現できる ← 技術用語3

**Verbalization Count**: 3
```

**週次集計例**:

| 日付 | Verbalization Count | 技術用語例 |
|---|---|---|
| 2/23（日） | 4 | ER図、外部キー、正規化、リレーション |
| 2/24（月） | 3 | add_reference、belongs_to、has_many |
| 2/25（火） | 5 | Active Record、マイグレーション、バリデーション、モデル、スキーマ |
| 2/26（水） | 2 | validates、presence |
| 2/27（木） | 4 | バリデーション、uniqueness、numericality、エラーメッセージ |
| 2/28（金） | 3 | コントローラ、アクション、ルーティング |
| 3/01（土） | 5 | CRUD、new、create、strong parameters、redirect_to |

**Verbalization Score = 26回**（目標20回以上達成）

---

### トラッキング指標: Reading Time（量）

**定義**: 週次Reading合計時間

**目標**: **180min/週**（既存目標）

**測定方法**:
- Sessions DBに記録（Reading Type）
- 週次レビューで合計

**役割**: プロセス指標（量が確保されているかを確認）

**注意**: 量だけでは品質は保証されない → Implementation RateとVerbalization Scoreで品質を測定

---

## 3. Sessions DBへの記録フォーマット

### 必須フィールド

| フィールド | 説明 | 記録例 |
|---|---|---|
| **Date** | 日付 | 2026-02-24 |
| **Start Time** | 開始時刻 | 09:00 |
| **End Time** | 終了時刻 | 09:30 |
| **Duration** | 時間（分） | 30 |
| **Type** | セッション種別 | Reading |
| **Deep Score** | 集中度（1-5） | 4 |
| **Task** | 読んだ内容 | Railsガイド「Active Record マイグレーション」 |
| **Notes** | 備考 | 外部キー制約、add_referenceメソッドを学んだ |

### 追加フィールド（KPI測定用）

| フィールド | 説明 | 記録例 |
|---|---|---|
| **Implementation Flag** | 実装で試したか | Yes / No |
| **Verbalization Count** | Daily ReviewのWhyで技術用語を使った回数 | 3 |
| **Reading Source** | 参照元の種類 | 公式ドキュメント / gem README / 技術記事 / 書籍 |

### 記録例（Sessions DB）

```csv
Date,Start Time,End Time,Duration,Type,Deep Score,Task,Notes,Implementation Flag,Verbalization Count,Reading Source
2026-02-24,09:00,09:30,30,Reading,4,Railsガイド「Active Record マイグレーション」,外部キー制約、add_referenceメソッドを学んだ,Yes,3,公式ドキュメント
```

---

## 4. 読み方のプロセス（統合フロー）

### Off Day朝9:00-9:30（30min）

```
前夜（23:00）: Daily Planで明日の実装テーマを特定 + Reading素材をブックマーク
  ↓
朝食後（9:00）: トリガー発動「朝食後→即Reading」
  ↓
9:00-9:05: ブックマークを開く、タイマー30min設定
  ↓
9:05-9:25: 目次ベース読み（公式ドキュメント/gem README）
  - 目次を見て、今日の実装に関連する章を特定（5min以内）
  - 該当章を通読（15min）
  - コード例があれば流し読み（完全理解は不要）
  ↓
9:25-9:30: Sessions DBに記録
  - Reading Type、30min、DS評価
  - Reading Source: 公式ドキュメント/gem README
  - Implementation Flag: 空欄（実装後に記録）
  ↓
9:30-12:00: 実装セッション（読んだ内容を試す）
  ↓
18:00-18:15: Daily Reviewの「Fact + Why」記録
  - Fact: 「〇〇について読んだ→実装で△△を試した」
  - Why: 技術用語を使って言語化（Verbalization Count記録）
  - Implementation Flag: Yes/No を Sessions DBに追記
```

### Shift Day帰宅後（15min）

```
出勤前朝5min: 帰宅後の1タスクを決定
  - 翌日の実装テーマ〇〇のドキュメント15min
  - Reading素材（URL/ページ番号）をメモ
  - スマホのリマインダーに設定
  ↓
帰宅後（18:30-18:45）: トリガー発動「着替え→即Reading」
  ↓
18:30-18:32: リマインダー確認、タイマー15min設定
  ↓
18:32-18:45: 目次ベース読み（軽負荷）
  - 公式ドキュメントの目次を眺める（5min）
  - 翌日使いそうなセクションを特定（5min）
  - 冒頭部分を流し読み（5min）
  ↓
18:45-18:48: Sessions DBに記録
  - Reading Type、15min、DS評価
  - Reading Source: 公式ドキュメント
  - Implementation Flag: No（予習のみ、翌日に試す予定）
  ↓
翌日朝（9:30-12:00）: 実装セッション（昨日読んだ内容を試す）
  ↓
翌日夕方（18:00-18:15）: Daily Review
  - Fact: 「昨日読んだ〇〇を今日試した」
  - Why: 技術用語を使って言語化
  - 昨日のSessions DBのImplementation Flag: Yes に更新
```

---

## 5. 測定とフィードバックループ

### 週次チェックリスト（毎週日曜の週次レビュー時）

#### 主KPI確認

- [ ] **Implementation Rate**: ___ %（目標: 80%以上）
  - Reading実施日数: ___ 日
  - Implementation Flag: Yes の日数: ___ 日
  - 計算: Yes日数 / Reading実施日数 × 100%

#### 副KPI確認

- [ ] **Verbalization Score**: ___ 回（目標: 週20回以上）
  - 各日のVerbalization Countを合計
  - 技術用語の使用例を確認

#### トラッキング指標確認

- [ ] **Reading Time**: ___ min（目標: 180min）
  - Off Day朝30min × 5日 = 150min
  - Shift Day帰宅後15min × 2日 = 30min
  - 合計: 180min

#### Reading Source内訳

- [ ] 公式ドキュメント: ___ 回
- [ ] gem/ライブラリのREADME: ___ 回
- [ ] 技術記事: ___ 回
- [ ] 技術書籍: ___ 回
- [ ] Stack Overflow/GitHub Issues: ___ 回

#### 品質確認

- [ ] 「参照すべきでない」基準を守ったか: Yes / No
  - 古い技術記事を避けたか
  - 時間制約時に深い本を避けたか
  - エラー解決時に技術書籍の通読を避けたか

---

### PIVOT基準（Week 3中間レビュー）

Week 3終了時点で以下の場合、Reading MethodologyをPIVOT:

| 指標 | GO基準 | PIVOT基準 | PIVOT対策 |
|---|---|---|---|
| **Implementation Rate** | ≥80% | 60-79% | Reading素材の選定基準を見直し（より実装直結型に） |
| **Verbalization Score** | ≥60回（3週合計） | 40-59回（3週合計） | Daily ReviewのWhyで意識的に技術用語を使う習慣づけ |
| **Reading Time** | ≥540min（3週合計） | 450-539min（3週合計） | トリガー発動率を見直し（Reading Trigger Design参照） |

### KILL基準（戦略的撤退）

以下の場合、Reading Methodologyを根本的に見直す:
- Implementation Rate < 60%
- Verbalization Score < 40回（3週合計）
- Reading Time < 450min（3週合計）

**KILL時の対策**:
- 読み方のアプローチを変更（目次ベース→実装駆動読み）
- Reading素材の種類を限定（公式ドキュメントのみ）
- 目標を下方修正（Implementation Rate 60%、Verbalization Score 週15回）

---

## 6. 習慣定着度の評価

### 6週間後の自己採点（OBL Cycle 2終了時）

| レベル | 状態 | 判定基準 |
|---|---|---|
| **5点** | 完全自動化 | Reading→実装→言語化が自然に循環、KPI測定が習慣化 |
| **4点** | ほぼ自動化 | Implementation FlagやVerbalization Countの記録が習慣化 |
| **3点** | 意識的実行 | 週次チェックリストを見ながら記録、時々忘れる |
| **2点** | 不安定 | KPI記録率60%以下、測定が機能していない |
| **1点** | 未定着 | KPI記録率30%以下、測定失敗 |

**目標**: Week 6終了時点で**レベル4以上**

---

## 7. 次のアクション

このReading Methodologyを実践するために必要な準備:

### 1. Daily Reviewテンプレートに「KPI記録欄」を追加

```markdown
## Daily Review - YYYY-MM-DD

### Fact
- [Time]: [Activity]
- **Implementation Flag**: Yes / No

### Why
- [Reason 1]
- [Reason 2]
- **Verbalization Count**: X
```

### 2. Sessions DBに「KPI記録フィールド」を追加

- Implementation Flag（Yes/No）
- Verbalization Count（数値）
- Reading Source（公式ドキュメント/gem README/技術記事/書籍/Stack Overflow）

### 3. 週次チェックリストをテンプレート化

- 週次レビュー時に自動でKPI集計できるようにする
- 過去週との比較グラフを作成

---

## 参照ドキュメント

- [Reading Trigger Design](reading_trigger_design.md): 「いつ読むか」（トリガー、タイミング、時間配分）
- [OBL戦略レポート](../../outputs/obl_strategy_report_2026-02-23.md): 全体戦略とJust-in-Time Learning
- [OBL Sprint Guide](../../OBL_sprint.md): フレームワークとPIVOT基準
- [OBL Sprint Lessons](../../obl_sprint_lessons_2026_q1.md): 前回サイクルからの教訓

---

**作成者**: Claude Sonnet 4.5
**レビュー**: 要
**ステータス**: Draft（Week 1で検証開始）
