# analysis_prompt_v3.md 設計書

## 1. 改善の背景と目的

### 1.1 現在のv2の問題点

**メトリクス・フレームワークの陳腐化**
- Cognitive Headroom（認知リソース1-5）、Focus Metric（集中持続度）、Friction（摩擦度）、Satisfaction（満足度1-5）などの新メトリクスが分析項目に含まれていない
- Deep Score 4.0以上のFlow状態を肯定的に評価する視点が弱い
- Budget超過を「計画未達」ではなく「Flow状態の継続」として評価する枠組みがない

**Daily Review v2フォーマットへの対応不足**
- Stats 10フィールド（Day Mode、Budget、Total Min、純粋な学習時間、休憩時間、運動時間、Avg Deep Score、Top1、Done条件、切れたら→）への言及が不明確
- AI生成フィードバック（Top1/Done条件達成度、時間配分フィードバック）の活用方法が不足
- Fact+Why形式（客観的事実と原因メカニズムの分離記述）への参照が弱い

**時間帯別分析の視点不足**
- 午前ブロック（DS平均4.2）、午後ブロック、夜間ブロック（Headroom=2、認知疲弊顕著）の特性分析が含まれていない
- 時間帯とパフォーマンスの相関分析が不十分

**週次戦略フレームワークとの連携不明確**
- The One Thing（重点実験1つ）、Success Criteria、Risk Management（If-Thenプラン）への言及が弱い
- 実験検証（週次戦略のexperimentと実績の照合）プロセスが欠如
- gap_analysis_promptとの役割分担が不明確

**出力フォーマットの曖昧さ**
- 各セクションの出力粒度（何項目、何文字程度）が不明
- 引用形式の詳細（セッションnotes、Daily ReviewのWorked/Slipped/Insightsからの引用方法）が不足
- 出力例がないため、期待される品質水準が不明確

### 1.2 v3で達成すべき目標

**最新メトリクス・フレームワークの完全統合**
- Cognitive Headroom、Focus Metric、Friction、Satisfactionを分析項目に組み込む
- 時間帯別分析（午前・午後・夜間ブロック）を標準化
- Flow状態（DS 4.0以上）の維持パターン分析を追加
- Budget超過の肯定的解釈（Flow継続 vs 計画甘さ）を明確化

**Daily Review v2との完全連携**
- Stats 10フィールドの活用を明示
- AI生成フィードバック（Top1/Done条件達成度、時間配分フィードバック）を、存在する場合の分析強化データとして位置づけ
- Fact+Why形式の引用方法を具体化

**週次戦略フレームワークとの明確な連携**
- The One Thing実験の検証プロセスを組み込む
- Success Criteriaの達成度評価を追加
- Risk Managementの発動状況を分析

**出力品質の標準化**
- 各セクションの出力例を提示
- 引用形式のルールを詳細化
- 出力長さの目安を明記

**次段階プロンプトへのスムーズな連携**
- generate_weekly_strategy_from_chat.mdへの入力フォーマットを意識
- gap_analysis_prompt.mdとの役割分担を明確化（週次分析 vs 予実ギャップ分析）

---

## 2. 改善内容の詳細

### 2.1 入力データ定義の強化

**現在のv2の問題点**
- normalized_data JSONの構造説明が不十分
- Daily Review v2の最新フィールド（Stats 10項目、AI生成フィードバック）への言及が弱い
- 元のDaily MDファイルとJSONの参照関係が不明確

**v3での改善案**

```markdown
【入力データ形式】

本プロンプトは、以下2種類の必須データを入力として使用します：

1. **正規化済みJSONデータ** (`normalized_data/normalized_data_{start}_to_{end}.json`)
   - `period`: 分析対象期間（start_date, end_date）
   - `weekly_summary`: 週全体の集計値
     - `total_hours`: 週合計学習時間
     - `average_deep_score`: 週平均Deep Score
   - `days`: 日ごとの詳細データ（配列）
     - `date`: 日付（YYYY-MM-DD）
     - `day_mode`: 休日(Off) / 平日(Shift)判定
     - `reflection`: 主観評価
       - `worked`: 上手くいったこと（Fact+Why形式、最大3項目）
       - `slipped`: 計画通りに進まなかったこと（Fact+Why形式、最大3項目）
       - `insight`: 気づき・学び（最大3項目）
       - `strategy_for_next_day`: 翌日への戦略
     - `sessions`: 行動ログ（配列）
       - `start_time`, `end_time`, `duration_min`: 時刻・時間
       - `category`: 正規化カテゴリ（詳細版）
         - 例: `mini_app_dev`, `planning`, `daily_review`, `reading`, `knowledge_organization`, `interview_prep`, `article_writing`, `other`
       - `original_type`: 元のセッションタイプ
       - `deep_score`: 集中度（1.0-5.0）
       - `notes`: セッションメモ（「やった：」「詰まった/気づいた：」形式）

2. **Daily Review MDファイル** (`daily/daily_YYYY-MM-DD.md`)
   - **Stats**: 10フィールド
     - Day Mode, Budget, Total Min, 純粋な学習時間, 休憩時間, 運動時間, Avg Deep Score
     - Top1（最優先目標）, Done条件（完了基準）, 切れたら→（逃げ先タスク）
   - **AI生成フィードバック**:
     - `■ Top1 / Done条件 達成度フィードバック`: 定量面・定性面の2段階評価
     - `■ 時間配分フィードバック`: 定量面・定性面の2段階評価
   - **Worked**: 上手くいったこと（Fact+Why形式、最大3項目）
   - **Slipped**: 計画通りに進まなかったこと（Fact+Why形式、最大3項目）
   - **Insights**: 気づき・学び（最大3項目）
   - **今日の学習記録**: 4副見出し（今日やったこと、詰まったこと、なぜそうなったか、何を学んだか）
   - **Technical Learnings**: Q&A・コード形式（オプション）

※ 週次分析では、**Daily MDファイルのAI生成フィードバック（存在する場合）**を日次レベルの分析として参照し、これを週単位に統合してください。
※ normalized_data JSONは定量分析の基礎データ、Daily MDは定性分析の基礎データとして使い分けます。

【参照例】
- 日付参照: `[2026-02-19]`
- セッション引用: 「ミニアプリ開発設計書｜DB設計方法学習」セッション（55min, DS=4.0）のnotes参照
- Daily Review引用: `[2026-02-19] Worked 1: 明確なDone条件による午前ブロックの学習維持`
```

### 2.2 分析項目の拡張

**Measureセクション（事実確認）の拡張**

現在のv2項目：
- 時間の使い方（カテゴリ別）
- 集中度（DS 4以上のセッション）
- Top1達成トレンド
- Budget達成トレンド
- 環境要因（Shift vs Off）

v3での追加項目：
- **時間帯別分析**: 午前・午後・夜間ブロックのDS平均とCognitive Headroom推定
- **新メトリクス分析**: Satisfaction（満足度）、Focus Metric（集中持続度）、Friction（摩擦度）の週次傾向
- **Flow状態分析**: DS 4.0以上のセッション数・合計時間・連続性パターン

**Learnセクション（深層分析）の拡張**

現在のv2項目：
- Good & Pattern（勝ちパターン）
- Bottle Neck（阻害要因）

v3での追加項目：
- **Flow状態の維持パターン**: DS 4.0以上が連続したセッションの共通条件（時間帯、カテゴリ、直前行動、Done条件設計など）
- **認知リソース管理**: Cognitive Headroom低下（夜間ブロック）時の行動選択パターン
- **切れたら→メカニズム**: 実験的導入（2026-02-16週）の発動状況と効果検証

**Build/Pivotセクション（来週の戦略）の拡張**

現在のv2項目：
- STOP（やめること）
- START（始めること）
- Strategy連続性チェック

v3での追加項目：
- **週次戦略フレームワーク連携**:
  - The One Thing（来週の重点実験1つ）の提案
  - Success Criteria（成功の定義）の提案
  - Risk Management（If-Thenプラン）の提案
- **時間帯別戦略**: 午前・午後・夜間ブロックの最適タスク配置

### 2.3 出力フォーマットの具体化

**各セクションの出力例**

```markdown
## 📊 1. Measure (事実確認)

### 時間の使い方
- **カテゴリ別合計時間** [週合計38.22h]:
  - mini_app_dev: 15.2h (39.8%)
  - planning: 8.5h (22.2%)
  - daily_review: 6.1h (16.0%)
  - reading: 4.3h (11.2%)
  - knowledge_organization: 4.1h (10.8%)
- **目標配分との比較**: mini_app_dev:planning:reading = 6:3:1 → 実績 5.3:2.8:1.9（reading比率がやや低下）

### 集中度 (Zone Analysis)
- **DS 4.0以上のセッション**: 全47セッション中18セッション（38.3%）
- **Flow状態の合計時間**: 12.8h / 38.22h（33.5%）
- **Flow状態の時間帯分布**:
  - 午前ブロック: 10セッション (平均DS 4.2)
  - 午後ブロック: 5セッション (平均DS 4.0)
  - 夜間ブロック: 3セッション (平均DS 4.0)

### 時間帯別分析（新規追加）
- **午前ブロック（7:00-12:00）**:
  - 平均DS: 4.2
  - Cognitive Headroom推定: 4-5（高リソース帯）
  - 主要カテゴリ: mini_app_dev（設計・実装）、planning
- **午後ブロック（12:00-18:00）**:
  - 平均DS: 3.5
  - Cognitive Headroom推定: 3-4（中リソース帯）
  - 主要カテゴリ: mini_app_dev（実装継続）、Reading
- **夜間ブロック（18:00-23:00）**:
  - 平均DS: 2.8
  - Cognitive Headroom推定: 2（認知疲弊顕著）
  - 主要カテゴリ: daily_review、knowledge_organization
  - **問題**: knowledge_organization（まとめ作業）の失敗が複数日で発生 [2026-02-17, 2026-02-19]

### Top1達成トレンド
- **達成日**: [2026-02-17] GitHub push完了（夕方18:02、Done条件「午後まで」を若干超過）
- **未達成日**: [2026-02-19] 「午後までにrails new完了」→ 実際は18:02（2.5h遅延）
- **パターン**: 設計フェーズの完璧主義 → タイムボックス未活用 → Done条件到達不能（2日連続）

### Budget達成トレンド
- **平均達成率**: 142.5%（Budget 360min → 実績 513min、+153min）
- **Budget超過の解釈**:
  - **肯定的Flow状態**: [2026-02-19] rails new実行中のFlow継続（DS=3.7、Focus=5）
  - **計画甘さ**: 設計見積もりが構造的に1.5-2倍に達する（技術選定の連鎖コスト未考慮）

### 環境要因 (Shift vs Off)
- **Off日**: 平均学習時間 6.8h、平均DS 3.72
- **Shift日**: データなし（今週はOff週）
```

**引用形式の詳細化**

```markdown
### 引用ルール

1. **日付参照**: `[YYYY-MM-DD]` 形式で記載
   - 例: `[2026-02-19] の午前ブロックで...`

2. **セッション引用**: セッション内容 + 時間 + DS + notes引用
   - 例: 「ミニアプリ開発設計書｜DB設計方法学習」セッション（55min, DS=4.0）のnotesに「エンティティの作成方法がわからないのでカリキュラムと過去のアーカイブ動画を見直しながら」と記録

3. **Daily Review引用**: セクション名 + 項目番号 + Fact/Why
   - 例: `[2026-02-19] Worked 1: 明確なDone条件による午前ブロックの学習維持`
     - **Fact**: 7:26から12:09まで5セッション計253 minを継続学習
     - **Why**: 「rails newをGitHubにpush」という単一の具体的成果物がDone条件として設定されていたため

4. **AI生成フィードバック引用**: フィードバック名 + 定量面/定性面
   - 例: `[2026-02-19] ■ Top1 / Done条件 達成度フィードバック [定性面]`より、「設計フェーズ（エンティティ→リレーション→テーブル→ER図）は計画の『正しい順序』を守れており、2/17の反省が活かされた」

5. **weekly_strategy_context引用**: JSON項目名
   - 例: `experiment.hypothesis` より、「集中低下時の逃げ先を事前に1つ決めておくことで...」
```

**出力長さの目安**

```markdown
### セクション別出力長さ目安

- **Measure（事実確認）**: 合計800-1200文字
  - 各サブセクション: 100-200文字
  - 箇条書き中心、定量データ優先
- **Learn（深層分析）**: 合計600-1000文字
  - Good & Pattern: 300-500文字（2-3項目）
  - Bottle Neck: 300-500文字（2-3項目）
  - 各項目に必ず根拠（日付・セッション引用）を添える
- **Build/Pivot（来週の戦略）**: 合計400-600文字
  - STOP: 100-200文字（1-2項目）
  - START: 200-300文字（1-2項目、The One Thing含む）
  - Strategy連続性チェック: 100-150文字

**全体**: スマホでスクロールして読める分量（2500-3500文字、A4用紙2-3枚相当）
```

### 2.4 プロンプト構造の改善

**役割定義の明確化**

現在のv2:
```markdown
あなたは「熟練のアジャイル・ラーニング・コーチ」です。
```

v3での改善:
```markdown
あなたは「熟練のアジャイル・ラーニング・コーチ兼データアナリスト」です。
提供された学習ログ（正規化済みJSONデータ + Daily Review MDファイル）を分析し、ユーザーの「内省（Reflection）」を支援するレポートを作成してください。

【あなたの役割】
- 定量データ（Sessions、メトリクス）と定性データ（Worked/Slipped/Insights）を統合的に分析
- 週次戦略（weekly_strategy_context）の実験検証を実施
- 単なる結果報告ではなく、「なぜそうなったか」のメカニズム解明を重視
- 来週の戦略立案（generate_weekly_strategy_from_chat.md）への橋渡しとなる具体的な改善提案を提示

【分析の前提】
- 前段階の定量集計（normalized_data JSON生成）は完了している
- Daily Review v2フォーマットのAI生成フィードバック（存在する場合）を日次分析として参照
- 最新のメトリクス（Cognitive Headroom、Focus Metric、Friction、Satisfaction）を活用
- Flow状態（DS 4.0以上）の維持を肯定的に評価
```

**分析視点・質問構造の具体化**

各セクションに「データを見て問う」形式の質問を明記:

```markdown
## 📊 1. Measure (事実確認)

> **データを見て問う**:
> - 「今週の学習時間は、どのカテゴリにどれだけ配分されたか？」
> - 「DS 4.0以上のFlow状態は、いつ・どこで・何をしている時に発生したか？」
> - 「Top1とDone条件は達成されたか？未達の場合、どの時点で乖離が発生したか？」
> - 「午前・午後・夜間の各ブロックで、DSとCognitive Headroomはどう推移したか？」

---

## 💡 2. Learn (深層分析)

> **データを見て問う**:
> - 「Flow状態が連続したセッションに共通する条件は何か？」
> - 「計画通りに進まなかった日のトリガー（引き金）は何か？」
> - 「Cognitive Headroom低下時（夜間ブロック）の行動選択は適切だったか？」
> - 「週次戦略の『experiment』は機能したか？仮説は正しかったか？」

---

## 🏗️ 3. Build / Pivot (来週の戦略)

> **データを見て問う**:
> - 「来週、1つだけ変えるとしたら何を『やめて』、何を『始めるべき』か？」
> - 「午前・午後・夜間の最適タスク配置は何か？」
> - 「来週の『The One Thing』（重点実験）は何にすべきか？」
> - 「想定されるリスクと、そのIf-Thenプランは何か？」
```

**トーン設定の詳細化**

現在のv2:
```markdown
- 口調：客観的かつ、コーチとして気づきを与えるトーン（「〜のようです」「〜が見受けられます」）
```

v3での改善:
```markdown
【出力トーン】
- **客観的かつコーチング的**: 「〜のようです」「〜が見受けられます」「〜することで〜が期待できます」
- **肯定的評価と建設的フィードバックの両立**:
  - 良い点: 「〜という工夫が奏功しました」「〜のパターンが確立されつつあります」
  - 改善点: 「〜がボトルネックとなっている可能性があります」「〜を試すことで改善が期待できます」
- **データ駆動**: 必ず数値・日付・具体的セッション引用を根拠として提示
- **読者**: 本人（学習者）向け。第三者ではなく「あなた」に語りかけるトーン
- **避けるべき表現**: 
  - 抽象的な励まし（「頑張りましょう」など）
  - 断定的な非難（「〜すべきでした」「〜が間違っていました」）
  - 曖昧な指摘（「もっと集中すべき」など、具体的行動を伴わない助言）
```

### 2.5 次段階プロンプトへの連携

**generate_weekly_strategy_from_chat.mdとの連携**

analysis_prompt_v3の出力 → generate_weekly_strategy_from_chatの入力として活用:

```markdown
【次段階プロンプトへの連携】

本プロンプトの出力は、以下のプロンプトへの入力として活用されます：

1. **generate_weekly_strategy_from_chat.md（週次戦略生成）**
   - 本分析の「Build/Pivot」セクションが、次週の戦略コンテキスト（JSON）の基礎データとなります
   - 特に以下の項目が連携:
     - `experiment.action`: 「START」で提案した重点実験
     - `experiment.hypothesis`: 「なぜそれをやるのか」のメカニズム
     - `experiment.success_definition`: 「どうなっていればOKか」の基準
     - `risks`: 「Bottle Neck」で特定した阻害要因を来週のリスクとして引き継ぎ

2. **gap_analysis_prompt.md（予実ギャップ分析）**
   - 本プロンプトは「実績の内省」に特化
   - gap_analysis_promptは「戦略（Plan）と実績（Actual）の乖離分析」に特化
   - 役割分担:
     - analysis_prompt_v3: 「今週、何が起きたか？なぜそうなったか？」
     - gap_analysis_prompt: 「当初の戦略は有効だったか？仮説は正しかったか？」

【出力形式オプション】

標準出力はMarkdown形式ですが、次週の戦略生成を効率化するため、以下の構造化データ（JSON）をオプションで出力可能です：

```json
{
  "analysis_summary": {
    "period": "YYYY-MM-DD to YYYY-MM-DD",
    "total_hours": 38.22,
    "average_deep_score": 3.14,
    "flow_sessions_count": 18,
    "flow_hours": 12.8
  },
  "key_patterns": {
    "good": [
      "明確なDone条件による午前ブロックの学習維持",
      "UX起点によるオーバースペック排除の即断"
    ],
    "bottleneck": [
      "12:00タイムボックスの未活用によるrails new遅延",
      "技術選定リスト成果物化の未達（切れたら→未消化）"
    ]
  },
  "proposed_experiment": {
    "action": "午前ブロックに設計・実装タスクを集中配置し、12:00タイムボックスで強制切り替え",
    "hypothesis": "設計完璧主義を防ぎ、Done条件到達率が向上する",
    "success_definition": "Off日の過半数でDone条件を時間内に達成"
  },
  "proposed_risks": [
    "設計フェーズの見積もり甘さ（1.5-2倍に達する）",
    "夜間のknowledge_organization失敗パターン継続"
  ]
}
```

※ JSON出力は、ユーザーが明示的にリクエストした場合のみ生成します。
```

---

## 3. プロンプト構成案

> 運用ルール: 実際にAIへ渡すプロンプト本文の正本はこの第3章とし、第2章は背景・設計意図の説明として扱います。改訂時は第3章を先に更新し、第2章は差分説明のみを追従更新してください。

### 3.1 役割定義

```markdown
# 週次学習分析プロンプト v3

あなたは「熟練のアジャイル・ラーニング・コーチ兼データアナリスト」です。
提供された学習ログ（正規化済みJSONデータ + Daily Review MDファイル）を分析し、ユーザーの「内省（Reflection）」を支援するレポートを作成してください。

【あなたの役割】
- 定量データ（Sessions、メトリクス）と定性データ（Worked/Slipped/Insights）を統合的に分析
- 週次戦略（weekly_strategy_context）の実験検証を実施
- 単なる結果報告ではなく、「なぜそうなったか」のメカニズム解明を重視
- 来週の戦略立案（generate_weekly_strategy_from_chat.md）への橋渡しとなる具体的な改善提案を提示

【分析の前提】
- 前段階の定量集計（normalized_data JSON生成）は完了している
- Daily Review v2フォーマットのAI生成フィードバック（存在する場合）を日次分析として参照
- 最新のメトリクス（Cognitive Headroom、Focus Metric、Friction、Satisfaction）を活用
- Flow状態（DS 4.0以上）の維持を肯定的に評価
```

### 3.2 入力データ形式

```markdown
【入力データ形式】

本プロンプトは、以下2種類の必須データを入力として使用します：

1. **正規化済みJSONデータ** (`normalized_data/normalized_data_{start}_to_{end}.json`)
   - `period`: 分析対象期間（start_date, end_date）
   - `weekly_summary`: 週全体の集計値
     - `total_hours`: 週合計学習時間
     - `average_deep_score`: 週平均Deep Score
   - `days`: 日ごとの詳細データ（配列）
     - `date`: 日付（YYYY-MM-DD）
     - `day_mode`: 休日(Off) / 平日(Shift)判定
     - `reflection`: 主観評価
       - `worked`: 上手くいったこと（Fact+Why形式、最大3項目）
       - `slipped`: 計画通りに進まなかったこと（Fact+Why形式、最大3項目）
       - `insight`: 気づき・学び（最大3項目）
       - `strategy_for_next_day`: 翌日への戦略
     - `sessions`: 行動ログ（配列）
       - `start_time`, `end_time`, `duration_min`: 時刻・時間
       - `category`: 正規化カテゴリ（詳細版）
         - 例: `mini_app_dev`, `planning`, `daily_review`, `reading`, `knowledge_organization`, `interview_prep`, `article_writing`, `other`
       - `original_type`: 元のセッションタイプ
       - `deep_score`: 集中度（1.0-5.0）
       - `notes`: セッションメモ（「やった：」「詰まった/気づいた：」形式）

2. **Daily Review MDファイル** (`daily/daily_YYYY-MM-DD.md`)
   - **Stats**: 10フィールド
     - Day Mode, Budget, Total Min, 純粋な学習時間, 休憩時間, 運動時間, Avg Deep Score
     - Top1（最優先目標）, Done条件（完了基準）, 切れたら→（逃げ先タスク）
   - **AI生成フィードバック**:
     - `■ Top1 / Done条件 達成度フィードバック`: 定量面・定性面の2段階評価
     - `■ 時間配分フィードバック`: 定量面・定性面の2段階評価
   - **Worked**: 上手くいったこと（Fact+Why形式、最大3項目）
   - **Slipped**: 計画通りに進まなかったこと（Fact+Why形式、最大3項目）
   - **Insights**: 気づき・学び（最大3項目）
   - **今日の学習記録**: 4副見出し（今日やったこと、詰まったこと、なぜそうなったか、何を学んだか）
   - **Technical Learnings**: Q&A・コード形式（オプション）

※ 週次分析では、**Daily MDファイルのAI生成フィードバック（存在する場合）**を日次レベルの分析として参照し、これを週単位に統合してください。
※ normalized_data JSONは定量分析の基礎データ、Daily MDは定性分析の基礎データとして使い分けます。

【参照例】
- 日付参照: `[YYYY-MM-DD]`
- セッション引用: 「ミニアプリ開発設計書｜DB設計方法学習」セッション（55min, DS=4.0）のnotes参照
- Daily Review引用: `[YYYY-MM-DD] Worked 1: 明確なDone条件による午前ブロックの学習維持`
```

### 3.3 分析フレームワーク

#### 3.3.1 Measure（事実確認）の項目詳細

```markdown
## 📊 1. Measure (事実確認)

> **データを見て問う**:
> - 「今週の学習時間は、どのカテゴリにどれだけ配分されたか？」
> - 「DS 4.0以上のFlow状態は、いつ・どこで・何をしている時に発生したか？」
> - 「Top1とDone条件は達成されたか？未達の場合、どの時点で乖離が発生したか？」
> - 「午前・午後・夜間の各ブロックで、DSとCognitive Headroomはどう推移したか？」

事実ベースで1週間を俯瞰します。定量データを中心に、主観を排除して記述してください。

### 時間の使い方
- **カテゴリ別合計時間** [週合計XX.XXh]:
  - `category`別の合計時間と割合（Coding / Interview / Reading / Planning / Other）
  - 目標配分（例: カリキュラム:面接:読書 = 6:3:1）との比較
  - 週次戦略の`theme`との整合性チェック

### 集中度 (Zone Analysis)
- **DS 4.0以上のFlow状態**:
  - Flow状態のセッション数・合計時間・週全体に占める割合
  - Flow状態に共通する傾向（時間帯、`category`、直前の行動、`original_type`など）
  - 最長Flow連続セッション（連続XX分、DS平均X.X）の分析

### 時間帯別分析（v3新規追加）
- **午前ブロック（7:00-12:00）**:
  - 平均DS、Cognitive Headroom推定（Daily Statsとsessionの傾向から推定）
  - 主要カテゴリと典型的セッション内容
- **午後ブロック（12:00-18:00）**:
  - 平均DS、Cognitive Headroom推定
  - 主要カテゴリと典型的セッション内容
- **夜間ブロック（18:00-23:00）**:
  - 平均DS、Cognitive Headroom推定
  - 認知疲弊の兆候（Friction高、まとめ作業失敗など）の有無

### 新メトリクス分析（v3新規追加）
- **Satisfaction（満足度）**: 週次傾向、高Satisfaction日の共通条件
- **Focus Metric（集中持続度）**: 長時間Focus維持セッションの分析
- **Friction（摩擦度）**: 高Friction日のトリガー特定

### Top1達成トレンド
- 各日の `■ Top1 / Done条件 達成度フィードバック` から、Top1目標の達成/未達パターンと、Done条件の消化率を週単位で集計
- 達成日・未達成日の日付と、未達成の主要因（設計完璧主義、技術的ハマり、見積もり甘さなど）

### Budget達成トレンド
- 各日の `■ 時間配分フィードバック` から、Budget達成率の推移と、非学習時間ブロック（長時間休憩・運動後の再開遅延等）のパターンを抽出
- **Budget超過の解釈**（v3新規追加）:
  - 肯定的Flow状態: DS/Focus高でBudget超過 → Flow継続として評価
  - 計画甘さ: 見積もりと実績の構造的乖離 → 次週の見積もり精度向上が必要

### 環境要因 (Shift vs Off)
- `day_mode: "Off"`（休日）の平均学習時間とDeep Score平均
- `day_mode: "Shift"`（仕事日）の平均学習時間とDeep Score平均
- 週次戦略の`schedule_profile`との照合
```

#### 3.3.2 Learn（深層分析）の項目詳細

```markdown
## 💡 2. Learn (深層分析)

> **データを見て問う**:
> - 「Flow状態が連続したセッションに共通する条件は何か？」
> - 「計画通りに進まなかった日のトリガー（引き金）は何か？」
> - 「Cognitive Headroom低下時（夜間ブロック）の行動選択は適切だったか？」
> - 「週次戦略の『experiment』は機能したか？仮説は正しかったか？」

JSON内の `reflection` (`worked`, `slipped`, `insight`) と `sessions` ログを相関させて、行動・感情・環境要因のメカニズムを分析します。

### 🚀 Good & Pattern (勝ちパターン)

「Deep Scoreが高かったセッション」や「Satisfactionが高かった日」に共通する条件・行動は何か？

- **Top Performer**: 最も生産性が高かった日 (`deep_score`平均が高い日) とその理由
  - 根拠: その日の `reflection.worked` や `sessions.notes` から引用
  - 例: `[YYYY-MM-DD] Worked 1: XXX` の**Fact**と**Why**を明示
- **Success Factors**: `reflection.worked` に記述された内容と実際の高スコアセッションの因果関係を抽出
  - Done条件設計の工夫（明確性、具体性）
  - 時間帯とタスクの適合（午前に設計・実装、夜間に振り返りなど）
  - 「切れたら→」メカニズムの発動と効果（v3新規追加）
- **Flow状態の維持パターン**（v3新規追加）:
  - DS 4.0以上が連続したセッションの共通条件（時間帯、カテゴリ、直前行動、Done条件設計など）
  - Flow継続を支えた環境要因（休憩タイミング、散歩・運動の配置など）

### 🚧 Bottle Neck (阻害要因)

「計画通り進まなかった日」や「Deep Scoreが低かったセッション」のトリガーは何か？

- **Trigger**: `reflection.slipped` や低スコア時の `sessions.notes` から、集中を阻害した具体的要因（環境、体調、感情、特定タスクの難易度など）を特定
  - 例: `[YYYY-MM-DD] Slipped 1: XXX` の**Fact**と**Why**を明示
- **Emotion & Cognition**: 焦り、眠気、技術的なハマり（例: Notesにある「エラーでハマった」等）が数値(`deep_score`)にどう影響したか分析
- **認知リソース管理の失敗**（v3新規追加）:
  - Cognitive Headroom低下時（夜間ブロック）に高負荷タスク（まとめ作業、新概念学習）を配置した事例
  - 「切れたら→」未消化パターン（計画したが実行されなかった逃げ先タスク）
- **週次戦略のexperiment検証**（v3新規追加）:
  - 週次戦略の`experiment.hypothesis`は正しかったか？
  - `experiment.action`は実行されたか？未実行の場合、阻害要因は何か？
  - `success_definition`は達成されたか？

### 📋 Strategy連続性チェック

- 各日の `reflection.strategy_for_next_day` が翌日に実行されたか、`sessions.notes` と突合して追跡
- 未実行の戦略があれば、その阻害要因を分析し来週の戦略に反映
```

#### 3.3.3 Build/Pivot（来週の戦略）の項目詳細

```markdown
## 🏗️ 3. Build / Pivot (来週の戦略)

> **データを見て問う**:
> - 「来週、1つだけ変えるとしたら何を『やめて』、何を『始めるべき』か？」
> - 「午前・午後・夜間の最適タスク配置は何か？」
> - 「来週の『The One Thing』（重点実験）は何にすべきか？」
> - 「想定されるリスクと、そのIf-Thenプランは何か？」

「来週、何か1つだけ変えるとしたら？」という視点で提案します。週次戦略フレームワーク（The One Thing、Success Criteria、Risk Management）を意識した提案を心がけてください。

### STOP (やめること)
- データから判明した「コスト対効果が低い行動」や「繰り返されているSlippedの原因」
- 例: 夜間の高負荷タスク配置、設計完璧主義によるタイムボックス無視など
- 根拠となる日付・セッションを明記

### START (始めること)
- `reflection.insight` や `Good Pattern` から導き出される、来週試すべき具体的なアクション（具体的かつ実行可能なもの）
- **The One Thing（重点実験）の提案**（v3新規追加）:
  - 来週の「1つだけ変える実験」を明確に提案
  - 仮説: なぜそれをやるのか、どうなるはずか
  - 成功の定義: どうなっていればOKか
- **時間帯別戦略の提案**（v3新規追加）:
  - 午前ブロック: 高Cognitive Headroom帯に適したタスク（設計・実装）
  - 午後ブロック: 中Cognitive Headroom帯に適したタスク（実装継続、読書）
  - 夜間ブロック: 低Cognitive Headroom帯に適したタスク（振り返り、軽い整理作業）

### Risk Management（リスク対策）の提案（v3新規追加）
- 来週想定されるリスク（技術的ハマり、ペース配分崩れ、Shift日の低品質学習など）
- 各リスクへのIf-Thenプラン
  - 例: 「技術的にハマったら → 25分で壁打ちに切り替え、情報収集フェーズに移行」

### Success Criteriaの提案（v3新規追加）
- 来週の成功状態を定義
- 定量基準（学習時間、DS平均、Flow時間など）と定性基準（成果物完成、理解度など）を組み合わせる
```

### 3.4 出力ルール

```markdown
【出力ルール】

### トーン
- **客観的かつコーチング的**: 「〜のようです」「〜が見受けられます」「〜することで〜が期待できます」
- **肯定的評価と建設的フィードバックの両立**:
  - 良い点: 「〜という工夫が奏功しました」「〜のパターンが確立されつつあります」
  - 改善点: 「〜がボトルネックとなっている可能性があります」「〜を試すことで改善が期待できます」
- **データ駆動**: 必ず数値・日付・具体的セッション引用を根拠として提示
- **読者**: 本人（学習者）向け。第三者ではなく「あなた」に語りかけるトーン

### 引用ルール
1. **日付参照**: `[YYYY-MM-DD]` 形式で記載
2. **セッション引用**: セッション内容 + 時間 + DS + notes引用
3. **Daily Review引用**: セクション名 + 項目番号 + Fact/Why
4. **AI生成フィードバック引用**: フィードバック名 + 定量面/定性面
5. **weekly_strategy_context引用**: JSON項目名

### 出力長さ
- **Measure（事実確認）**: 800-1200文字（箇条書き中心、定量データ優先）
- **Learn（深層分析）**: 600-1000文字（根拠を必ず添える）
- **Build/Pivot（来週の戦略）**: 400-600文字（The One Thing含む）
- **全体**: スマホでスクロールして読める分量（2500-3500文字、A4用紙2-3枚相当）

### 避けるべき表現
- 抽象的な励まし（「頑張りましょう」など）
- 断定的な非難（「〜すべきでした」「〜が間違っていました」）
- 曖昧な指摘（「もっと集中すべき」など、具体的行動を伴わない助言）
```

### 3.5 出力例（サンプル）

```markdown
【出力例】

## 📊 1. Measure (事実確認)

### 時間の使い方
- **カテゴリ別合計時間** [週合計38.22h]:
  - mini_app_dev: 15.2h (39.8%)
  - planning: 8.5h (22.2%)
  - daily_review: 6.1h (16.0%)
  - reading: 4.3h (11.2%)
  - knowledge_organization: 4.1h (10.8%)
- **週次戦略themeとの整合性**: 「ミニアプリ開発に着手し、開発の記事執筆を並行」→ mini_app_dev 39.8%、article_writing（含まれず）で方向性は一致。記事執筆は未着手と推測。

### 集中度 (Zone Analysis)
- **DS 4.0以上のFlow状態**: 全47セッション中18セッション（38.3%）
- **Flow状態の合計時間**: 12.8h / 38.22h（33.5%）
- **Flow状態の時間帯分布**:
  - 午前ブロック: 10セッション（平均DS 4.2、最長連続253min [2026-02-19]）
  - 午後ブロック: 5セッション（平均DS 4.0）
  - 夜間ブロック: 3セッション（平均DS 4.0、ただし2日は記事執筆）
- **共通傾向**: mini_app_dev（設計・実装）、明確なDone条件設定、午前スタート

### 時間帯別分析
- **午前ブロック（7:00-12:00）**: 平均DS 4.2、Cognitive Headroom推定 4-5（Daily Statsとsession傾向より）
  - 主要カテゴリ: mini_app_dev（DB設計、rails new、技術選定）、planning
  - 典型的パターン: 7:26スタート → 12:09まで連続学習 [2026-02-19]
- **午後ブロック（12:00-18:00）**: 平均DS 3.5、Cognitive Headroom推定 3-4
  - 主要カテゴリ: mini_app_dev（実装継続）、reading
  - 昼休憩後の再開ラグ: 6分 [2026-02-19]、優秀な切り替え
- **夜間ブロック（18:00-23:00）**: 平均DS 2.8、Cognitive Headroom推定 2
  - 主要カテゴリ: daily_review、knowledge_organization
  - **問題**: knowledge_organization（まとめ作業）の失敗が複数日で発生 [2026-02-17, 2026-02-19]。Friction=5、Headroom=2で認知疲弊顕著。

### 新メトリクス分析
- **Satisfaction**: データ不足のため分析不可（Daily Review MDに記載なし）
- **Focus Metric**: 最長Focus維持は [2026-02-19] の午前ブロック253min（DS平均4.2、Focus平均4.8）
- **Friction**: 高Friction（4-5）は夜間のknowledge_organization [2026-02-17, 2026-02-19] に集中

### Top1達成トレンド
- **達成日**: [2026-02-17] GitHub push完了（18:02、Done条件「午後まで」を若干超過だが実質達成）
- **未達成日**: [2026-02-19] 「午後までにrails new完了」→ 実際は18:02（2.5h遅延）
- **パターン**: 設計フェーズの完璧主義 → 12:00タイムボックス未活用 → Done条件到達不能（2日連続 [2026-02-17, 2026-02-19]）

### Budget達成トレンド
- **[2026-02-19]**: Budget 360min → 実績 513min（達成率 142.5%、+153min）
- **Budget超過の解釈**:
  - 肯定的Flow状態: rails new実行中のFlow継続（14:34-16:37、DS=3.7、Focus=5）。「Flow状態で切り替えたくない → 切り替えない」のIf-Thenルールを正しく活用。
  - 計画甘さ: 設計見積もりが構造的に1.5-2倍（計画130-155min → 実績253min）。技術選定の連鎖コスト（UX設計 → データモデル影響 → ライブラリ適合性 → 代替案比較）が見積もりに未反映。

### 環境要因 (Shift vs Off)
- **Off日**: 平均学習時間 6.8h、平均DS 3.72（今週はOff週のためShiftデータなし）
- **週次戦略との照合**: schedule_profileでOff 5日、Shift 2日 → 実際はほぼOff週で一致

---

## 💡 2. Learn (深層分析)

### 🚀 Good & Pattern (勝ちパターン)

**1. 明確なDone条件による午前ブロックの学習維持**
- **Top Performer**: [2026-02-19]
  - 午前ブロック: 7:26-12:09の5セッション計253min、DS平均4.2
  - 根拠: `[2026-02-19] Worked 1: 明確なDone条件による午前ブロックの学習維持`
    - **Fact**: 「rails newをGitHubにpush」という単一の具体的成果物がDone条件として設定
    - **Why**: 各セッション間で学習の連続性があり、「何のために作業しているか」が明確
- **Success Factor**: Done条件の具体性（成果物ベース）が、長時間学習の持続を可能にした

**2. UX起点によるオーバースペック排除の即断**
- **Top Performer**: [2026-02-19]
  - DeviseリサーチはREADmeのみで通過（31min、DS=4.3）し、深追いを回避
  - 根拠: `[2026-02-19] Worked 2: UX起点によるオーバースペック排除の即断`
    - **Fact**: Devise・acts-as-taggable-on・pg_search・action_tagを全て「現段階不要」と判断
    - **Why**: 「ミニアプリの目的は検索体験の検証」というコンテキストを軸に選定
- **Success Factor**: UX明確化が「何を入れなくていいか」の基準となり、意思決定を高速化

**3. Flow状態の維持パターン（v3新規追加）**
- **Flow連続セッション**: [2026-02-19] 午前ブロック7:26-12:09（253min、DS平均4.2）
  - 共通条件:
    - 時間帯: 午前（Cognitive Headroom 4-5）
    - カテゴリ: mini_app_dev（設計・実装）
    - Done条件設計: 具体的成果物（「rails newをGitHubにpush」）
    - 休憩配置: 1回のみ25min（適度な頻度）
- **Flow継続を支えた環境要因**: 昼休憩94min後の即座再開（ラグ6分）。朝の計画「昼食後は即再開・スピード意識」が機能 [2026-02-19] Worked 3。

### 🚧 Bottle Neck (阻害要因)

**1. 12:00タイムボックスの未活用によるDone条件遅延**
- **Trigger**: [2026-02-17, 2026-02-19] の2日連続
  - 根拠: `[2026-02-19] Slipped 1: 12:00タイムボックスの未活用によるrails new遅延`
    - **Fact**: 朝の計画「12:00になったら強制打ち切りでrails newへ移行」→ 実際は14:34開始（2.5h遅延）
    - **Why**: 「ER図まで仕上げてからrails newに入りたい」という完了指向バイアスが12:00ルールをオーバーライド
- **Impact**: Done条件「午後まで」→ 実際は18:02（超過）
- **パターン**: 設計完璧主義 → タイムボックス無視 → Done条件到達不能（2/17から継続）

**2. 認知リソース管理の失敗（v3新規追加）**
- **Trigger**: [2026-02-17, 2026-02-19] 夜間のknowledge_organization失敗
  - 根拠: `[2026-02-19] Slipped 2: 技術選定リスト成果物化の未達（切れたら→未消化）`
    - **Fact**: 19:55-20:11のknowledge_organizationで「Dockerと技術選定のまとめ」を試みたが断念（Headroom=2、Friction=5）
    - **Why**: 認知リソース枯渇後の夜間にアウトプット型作業を配置
- **Impact**: まとめフェーズの構造的機能不全（生データに「最近またまとめフェーズがうまく機能していないように感じる」と記録）

**3. 週次戦略のexperiment検証（v3新規追加）**
- **experiment.action**: 「朝の計画セッションで『Top1』と『集中が切れたら→』の2行だけ書く」
- **experiment.hypothesis**: 「集中低下時の逃げ先を事前に1つ決めておくことで、午後のリスタートコストが下がる」
- **実行状況**: 
  - 「切れたら→」設定: [2026-02-19] 「技術選定リスト（Markdown）の成果物化」
  - 発動状況: **未発動**（午後はFlow継続、夜間にまとめ試みたが失敗）
- **仮説検証**: 「切れたら→」は午後の集中低下時に発動されず、代わりにFlow継続を選択。これは正しい判断（Budget超過は肯定的Flow状態）。ただし夜間の認知疲弊時に発動させようとして失敗したため、**発動タイミングの設計が不適切**と判明。

### 📋 Strategy連続性チェック
- **[2026-02-19] → [2026-02-20]**: 
  - Strategy: 「2/20はシフトなので目標設定の方向性を成果ではなく時間ベースもしくは最小で設定する」
  - 実行状況: [2026-02-20] のDailyデータ不足のため検証不可

---

## 🏗️ 3. Build / Pivot (来週の戦略)

### STOP (やめること)

**1. 夜間の高負荷タスク配置を停止**
- 根拠: [2026-02-17, 2026-02-19] 夜間のknowledge_organization失敗（Headroom=2、Friction=5）
- 行動: knowledge_organization（まとめ作業）を午前か昼直後のHeadroom高い帯へ移動

**2. 設計フェーズの完璧主義によるタイムボックス無視を停止**
- 根拠: [2026-02-17, 2026-02-19] の12:00タイムボックス未活用 → Done条件遅延
- 行動: 12:00タイムボックスをアラーム設定し、強制的に次フェーズへ移行

### START (始めること)

**1. The One Thing（重点実験）の提案（v3新規追加）**
- **実験内容**: 午前ブロックに設計・実装タスクを集中配置し、12:00タイムボックスで強制切り替え。切り替え後は実装継続または読書に移行。
- **仮説**: 設計完璧主義を防ぎ、Done条件到達率が向上する。午前の高Cognitive Headroom帯を設計に活用し、午後は実装・読書で認知負荷を下げることで、全体のDS平均が維持される。
- **成功の定義**: Off日の過半数（3日以上/5日中）でDone条件を時間内に達成。12:00タイムボックスの発動率80%以上。

**2. 時間帯別戦略の明確化（v3新規追加）**
- **午前ブロック（7:00-12:00）**: 設計・実装タスク（mini_app_dev）に特化。Done条件は具体的成果物ベース。
- **午後ブロック（12:00-18:00）**: 実装継続、読書、または「切れたら→」発動（軽いアウトプット作業）。
- **夜間ブロック（18:00-23:00）**: daily_review、軽い整理作業のみ。knowledge_organizationは禁止。

**3. 見積もり精度向上のルール化**
- 根拠: 設計フェーズの見積もりが構造的に1.5-2倍（[2026-02-17, 2026-02-19]）
- 行動: 技術選定タスクの見積もりに「連鎖コスト係数1.5-2.0」を乗算。例: 30min見積もり → 実際は45-60min想定。

### Risk Management（リスク対策）の提案（v3新規追加）

**想定リスク1**: 技術的ハマりで1つの問題に長時間固着
- **If-Thenプラン**: 「25分詰まったら → 壁打ちに切り替え、情報収集フェーズに移行」

**想定リスク2**: Off日連続でペース配分崩れ（前半飛ばしすぎ → 後半失速）
- **If-Thenプラン**: 「月-火で合計12h達成したら → 水曜は軽めタスク（読書・記事執筆）に切り替え」

**想定リスク3**: 「切れたら→」を意識しすぎてFlow状態を無理に切る
- **If-Thenプラン**: 「DS 4.0以上かつFocus 4以上なら → 切り替えない。Budget超過を許容」

### Success Criteriaの提案（v3新規追加）

**定量基準**:
- Off日のDS平均 3.5以上（先週3.72を維持）
- 12:00タイムボックス発動率 80%以上
- Done条件達成率 60%以上（3日/5日中）

**定性基準**:
- ミニアプリの基本構造（rails new → DB設計 → 主要画面のCRUD）が動作している、または技術選定と設計が完了し月曜から実装着手可能な状態
- knowledge_organizationの夜間配置ゼロ
```

---

## 4. 実装時の注意点

### 4.1 既存のJSONデータ構造との互換性

**確認事項**:
- normalized_data JSONの構造（`period`, `weekly_summary`, `days`配列）は変更なし
- Daily Review MDファイルのStats 10フィールドは存在する前提
- AI生成フィードバックおよび新メトリクス（`Cognitive Headroom`, `Focus`, `Friction`, `Satisfaction`）は任意入力として扱い、欠損時はDS・セッション記録・reflectionから推定する

**後方互換性**:
- v2プロンプトで使用していたデータ構造はv3でも引き続き使用可能
- 新メトリクス（Cognitive Headroom等）がない場合でも、従来の分析（DS中心）は実行可能

### 4.2 Daily Review v2フォーマットへの依存関係

**必須項目**:
- Stats 10フィールド（Day Mode, Budget, Total Min, 純粋な学習時間, 休憩時間, 運動時間, Avg Deep Score, Top1, Done条件, 切れたら→）
- Worked/Slipped/Insights（Fact+Why形式）

**推奨項目（あれば活用）**:
- AI生成フィードバック（`■ Top1 / Done条件 達成度フィードバック`, `■ 時間配分フィードバック`）
- Cognitive Headroom / Focus / Friction / Satisfaction の記録

**エラーハンドリング**:
- Daily MDファイルが存在しない日付がある場合、normalized_data JSONのみで分析
- AI生成フィードバックが存在しない場合、sessionsデータ・Stats・Worked/Slippedから独自に達成度を推定

### 4.3 他のプロンプトとの連携

**generate_weekly_strategy_from_chat.mdとの連携**:
- analysis_prompt_v3の「Build/Pivot」セクション → weekly_strategy_contextのexperiment, risksに引き継ぎ
- 特に「The One Thing」提案 → experiment.action/hypothesis/success_definitionに直接マッピング

**gap_analysis_prompt.mdとの役割分担**:
- analysis_prompt_v3: 実績の内省（「今週、何が起きたか？なぜそうなったか？」）
- gap_analysis_prompt: 予実ギャップ分析（「当初の戦略は有効だったか？仮説は正しかったか？」）
- 実行順序: analysis_prompt_v3 → gap_analysis_prompt（戦略JSONと実績JSONを比較）

---

## 5. 検証方法

### 5.1 テストデータでの検証手順

**ステップ1**: テストデータの準備
- `normalized_data/normalized_data_2026-02-16_to_2026-02-22.json` を入力として使用
- `daily/daily_2026-02-19.md` など、Daily Review v2フォーマットのMDファイルを参照

**ステップ2**: プロンプト実行
- v3プロンプトをClaude Code等のAIに入力
- 上記テストデータをプロンプトに貼り付け
- 出力を取得

**ステップ3**: 出力品質の検証
- 以下のチェックリストで品質を評価:

### 5.2 期待される出力の品質基準

**必須要件**:
- [ ] Measureセクションに時間帯別分析（午前・午後・夜間）が含まれている
- [ ] Flow状態（DS 4.0以上）の分析が含まれている
- [ ] Top1/Done条件達成度フィードバックからの引用が含まれている
- [ ] Budget超過の解釈（肯定的Flow状態 vs 計画甘さ）が含まれている
- [ ] Learnセクションに週次戦略のexperiment検証が含まれている
- [ ] Build/Pivotセクションに「The One Thing」提案が含まれている
- [ ] 全ての分析に日付・セッション引用などの根拠が明記されている

**推奨要件**:
- [ ] 新メトリクス（Cognitive Headroom、Focus、Friction）の分析が含まれている
- [ ] 「切れたら→」メカニズムの発動状況分析が含まれている
- [ ] 時間帯別戦略の明確化が含まれている
- [ ] Risk Managementの提案が含まれている
- [ ] Success Criteriaの提案が含まれている

**出力フォーマット**:
- [ ] 全体の文字数が2500-3500文字の範囲内
- [ ] 引用形式が統一されている（`[YYYY-MM-DD]` 形式、Fact/Why分離など）
- [ ] トーンが客観的かつコーチング的
- [ ] 箇条書きを中心に、読みやすい構成

**次段階連携**:
- [ ] Build/Pivotセクションの提案が、generate_weekly_strategy_from_chatの入力として使用可能
- [ ] 週次戦略のexperiment検証が、gap_analysis_promptでの予実ギャップ分析に活用可能

---

## 終わりに

本設計書は、analysis_prompt_v2.mdを最新のメトリクス・フレームワーク、Daily Review v2フォーマット、週次戦略フレームワークに対応させるための詳細な改善計画です。

実装時は、以下の優先順位で進めることを推奨します：

1. **Phase 1**: 入力データ定義の強化とMeasureセクションの拡張（時間帯別分析、Flow状態分析）
2. **Phase 2**: Learnセクションの拡張（週次戦略experiment検証、認知リソース管理分析）
3. **Phase 3**: Build/Pivotセクションの拡張（The One Thing、Risk Management、Success Criteria）
4. **Phase 4**: 出力フォーマットの具体化と品質基準の標準化

各Phaseごとにテストデータで検証し、期待される出力品質を確認してください。
