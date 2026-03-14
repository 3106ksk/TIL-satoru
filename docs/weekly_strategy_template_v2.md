# 週次戦略テンプレート v2.0（実装中心型学習スタイル対応版）

**更新日**: 2026-03-09
**変更点**: 従来の「Reading強制」を廃止し、実装中心型学習スタイルに最適化。新指標体系（Learning Density、Conceptual Breakthrough、Output-Driven Learning）を統合。

---

## テンプレート使用方法

1. `[YYYY-MM-DD]`等のプレースホルダーを実際の値に置き換える
2. `schedule_profile`を実際のシフトスケジュールに合わせて修正
3. `theme`、`daily_top1`を週次目標に合わせて設計
4. `success_criteria`の数値目標を過去の実績に基づいて調整

---

# 週次戦略: Week [N] ([YYYY-MM-DD] to [YYYY-MM-DD])

**OBLスプリント**: [スプリントのテーマ]
**Phase**: [実装フェーズ / 学習フェーズ / 仕上げフェーズ]

---

## 1. 週末分析用データ (JSON)

```json
{
  "weekly_strategy_context": {
    "period": {
      "start": "[YYYY-MM-DD]",
      "end": "[YYYY-MM-DD]"
    },
    "theme": "[週次テーマ: 例「Tips CRUD完成 + カテゴリ機能 + daisyUI統合」]",
    "schedule_profile": {
      "sun": "[Off / Shift 時間帯]（[MM/DD]）",
      "mon": "[Off / Shift 時間帯]（[MM/DD]）",
      "tue": "[Off / Shift 時間帯]（[MM/DD]）",
      "wed": "[Off / Shift 時間帯]（[MM/DD]）",
      "thu": "[Off / Shift 時間帯]（[MM/DD]）",
      "fri": "[Off / Shift 時間帯]（[MM/DD]）",
      "sat": "[Off / Shift 時間帯]（[MM/DD]）"
    },
    "target_resources": {
      "total_hours_goal": 24.0,
      "estimated_available": "[XX.X]",
      "calculation_basis": "Off [N]日 × 5.5h = [XX]h + Shift(8-17) [N]日 × 1.5h = [XX]h + Shift(13-22) 午前ブロック [N]日 × 4h = [XX]h → 合計約[XX]h（バッファ[X]h）",
      "focus_time": "[集中可能な日の説明: 例「日〜火の3連続Off日（実装集中ゾーン）+ 土曜Off（仕上げ）」]"
    },
    "experiment": {
      "action": "[今週試す実験: 例「午前ブロックを100%Top1に集中投下する」]",
      "hypothesis": "[仮説: 例「午前ゴールデンタイムをTop1に集中投下することで、Done条件達成率が向上する」]",
      "success_definition": "[成功の定義: 例「Off日の過半数（3日以上/5日中）でTop1のDone条件を時間内に達成」]",
      "knowledge_organization_2stage": "**日報の2段階設計（knowledge_organization再設計）**\n\n| タイミング | 内容 | 目安時間 |\n|-----------|------|---------|\n| 夜（学習終了後） | 「今日やったこと・詰まったこと」の事実記録のみ | 10〜15分 |\n| 翌朝（計画セッション前） | 夜のメモを見ながら「なぜそうなったか・何を学んだか」を加筆 | 15〜20分 |\n| 不定期（週1） | 言語化できたと判断した回をNotion公開（アウトプット素材化） | 随時 |\n\n夜間knowledge_organizationの固定枠は廃止。朝の計画セッションに15〜20分を加算し、合計30〜40分の朝セッションに再設計。夜は認知負荷を下げて確実に事実記録のみを完了させる。"
    },
    "risks": [
      "[リスク1: 例「朝の計画セッションが30-40minを超過し、Top1着手が遅延」] → If-Then: [対策: 例「計画セッション30min経過時点で未完了なら、残りは午後に回し即座にTop1に切り替え」]",
      "[リスク2: 例「技術的ハマりで1つの問題に長時間固着」] → If-Then: [対策: 例「30分詰まったらClaude Codeで既存実装を解析、それでも解決しない場合は技術面談に切り替え」]",
      "[リスク3] → If-Then: [対策]",
      "[リスク4] → If-Then: [対策]"
    ],
    "daily_top1": {
      "day1": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名]",
        "done_condition": "[Done条件: 具体的成果物ベース]",
        "expected_contextual_learning": "[期待される学習ポイント: 例「Active Recordのアソシエーション、N+1問題」]"
      },
      "day2": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名]",
        "done_condition": "[Done条件]",
        "expected_contextual_learning": "[期待される学習ポイント]"
      },
      "day3": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名]",
        "done_condition": "[Done条件]",
        "expected_contextual_learning": "[期待される学習ポイント]"
      },
      "day4": {
        "date": "[MM/DD]",
        "top1": "[Shift日の場合: 技術記事執筆 or 実装継続（optional）]",
        "done_condition": "[Done条件: アウトプット成果物ベース or 実装成果物ベース]",
        "category": "[Reflective Output (optional) or Implementation]"
      },
      "day5": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名]",
        "done_condition": "[Done条件]",
        "expected_contextual_learning": "[期待される学習ポイント]"
      },
      "day6": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名]",
        "done_condition": "[Done条件]",
        "expected_contextual_learning": "[期待される学習ポイント]"
      },
      "day7": {
        "date": "[MM/DD]",
        "top1": "[Top1タスク名 + 週次まとめ]",
        "done_condition": "[Done条件 + 週次レビュー完成]",
        "expected_contextual_learning": "[期待される学習ポイント]"
      }
    },
    "success_criteria": {
      "quantitative": {
        "weekly_hours": "24h以上",
        "ds_average": "3.3以上",
        "total_input_hours": "6h以上（内訳: Focused Reading 1h + Contextual Learning 3h + Reflective Output 2h）"
      },
      "qualitative": {
        "learning_density": "DS4.0以上のContextual Learningセッション週3回以上",
        "conceptual_breakthrough": "Daily ReviewのInsights記述週3個以上",
        "output_driven_learning": "技術記事1本以上 or Technical Learnings更新3回以上 or 高品質knowledge_organization 2回以上"
      },
      "implementation": {
        "feature_completion": "週次themeで定義された機能の80%以上完了",
        "top1_achievement": "Top1タスクのDone条件を週5日以上でクリア（部分達成含む80%以上）"
      },
      "optional": {
        "technical_interview": "1回（3段階プロセス完了）※必須ではないが推奨",
        "focused_reading": "Railsガイド or 技術書を1章以上読了 ※optionalだが、体系的学習の機会として推奨"
      }
    }
  }
}
```

---

## 2. コーチからの戦略アドバイス

### Scope & Pace

[週間見込み時間とバッファの分析。例:]

お前の週間見込みは約[XX]h、目標は24h。**約[X]hのバッファがある**。[バッファの解釈とペース設計のアドバイス]

[実装タスクの配分分析。例:]

実装タスクが[日程]に集中している一方、[日程]は[Shift/その他理由]でモメンタムが途切れる可能性がある。具体的な対策:
- **[前日]のNight Reviewで、[翌日]のTop1タスクの着手手順まで書き出しておく**
- [Shift日等の制約がある日]は「[軽いタスク: 例「技術記事執筆30min」]」に限定し、エネルギーは温存する

### Risk Mitigation（If-Thenプラン）

| トリガー | Then（行動） |
|---|---|
| [リスクシナリオ1: 例「朝の計画セッションが30min超過」] | [対策: 例「残りは午後に回し、即座にTop1に切り替え」] |
| [リスクシナリオ2: 例「技術的ハマりで2h以上進まない」] | [対策: 例「Claude Codeで既存実装解析→技術面談に切り替え」] |
| [リスクシナリオ3] | [対策] |
| [リスクシナリオ4] | [対策] |

### Focus：今週の重点実験を成功させるためのマインドセット

[今週のexperimentに関連するマインドセット。例:]

お前が今週試みているのは、**「[実験の本質: 例「午前ゴールデンタイムをTop1に100%充当すること」]」**だ。

意識すべきは一つだけ：**「[核心的な行動指針: 例「Done条件を満たしたら、次へ進む」]」**。

[完璧主義を避けるアドバイス。例:]

完璧な[何か]を追い求めない。[具体例: 例「Day 1でマイグレーションが通ったら、それはDoneだ」]。**「動いた」を確認した瞬間に、次のタスクへ切り替えろ**。

初週で最も危険なのは、「もう少し良くしたい」という衝動に時間を奪われること。リファクタリングも最適化もWeek 3以降にいくらでもできる。今週の仕事は、**[今週の核心的ゴール]**。それ以上でも以下でもない。

---

## 3. 週内タイムライン（視覚化）

```
         [日程の性質を説明: 例「実装集中ゾーン」「Shift」「仕上げ」]
Sun ━━━━━━━━━━━━━━━━━━━━━━━━━ [Off / Shift]
Mon ━━━━━━━━━━━━━━━━━━━━━━━━━ [Off / Shift]
Tue ━━━━━━━━━━━━━━━━━━━━━━━━━ [Off / Shift]
Wed ░░░░░ Shift [時間帯] ░░░░░░ → 帰宅後 [optional活動: 例「技術記事執筆30min」]
Thu ░░░░░ Shift [時間帯] ░░░░░░ → 帰宅後 [optional活動: 例「Focused Reading 30min」]
Fri ━━━━ AM実装 ━━━━ ░░░░░░░░ Shift [時間帯] ░░░░░░░
Sat ━━━━━━━━━━━━━━━━━━━━━━━━━ [Off / Shift]
    ━━━ = 学習可能   ░░░ = Shift
```

**重要**: 水木のShift日帰宅後は「技術記事執筆」「Focused Reading」を**optional**とする。実装には手を出さない（モメンタム温存）。

---

## 4. 技術面談プラン（optional）

- **予定日**: [日程候補: 例「Day 2-3 (MM/DD-MM/DD、月火Off)」]
- **相談内容**: [技術テーマ: 例「アソシエーション設計のレビュー、正規化の妥当性」]
- **Prep (20min)**: [準備内容: 例「ER図を紙に描き、『なぜこの構造にしたか』を3文で言語化」]
- **実施 (30min)**: [面談での質問内容: 例「ER図を見せながら設計意図を説明 → FBを受ける」]
- **WrapUp (15min)**: [面談後の振り返り: 例「FBを箇条書き3点に要約 → 24h以内実践タスクを1つ決定」]

**Note**: 技術面談は必須ではないが、技術的判断に迷った場合や設計レビューが必要な場合は積極的に活用すること。

---

## 5. 新指標の週次目標

### Learning Density（学習密度）

**目標**: DS 4.0以上のContextual Learningセッションを週3回以上記録

**計測方法**:
- Sessions DBのnotesに`[Contextual Learning]`タグがあるセッションを抽出
- そのうちDS 4.0以上のセッション数をカウント

**Week Nでの具体的ターゲット**:
- [日付]: [期待される高集中学習セッション: 例「session概念解析」]
- [日付]: [期待される高集中学習セッション: 例「複雑なクエリ最適化」]
- [日付]: [期待される高集中学習セッション: 例「認証フローの仕組み理解」]

### Conceptual Breakthrough（概念のブレークスルー）

**目標**: Daily ReviewのInsights記述を週3個以上記録

**計測方法**:
- Daily ReviewのInsightsセクションに技術概念の理解記述があるかをカウント
- 「○○概念が腑に落ちた」「なぜ○○が必要か理解した」等の記述

**Week Nでの期待されるBreakthrough**:
- [期待される概念理解1: 例「Active Recordのアソシエーションの内部動作」]
- [期待される概念理解2: 例「sessionとcookieの役割分担」]
- [期待される概念理解3: 例「N+1問題の本質と解決策」]

### Output-Driven Learning（アウトプット駆動型学習）

**目標**: 技術記事1本以上 or Technical Learnings更新3回以上 or 高品質knowledge_organization 2回以上

**計測方法**:
- 技術記事: 外部公開（Qiita、Zenn等）または下書き完成（800字以上）
- Technical Learnings: `notes/`内のMD更新
- 高品質knowledge_organization: DS 3.5以上かつFriction 3以下、または完成した成果物あり

**Week Nでの具体的ターゲット**:
- [アウトプット候補1: 例「技術記事: sessionとcookieの違いまとめ」]
- [アウトプット候補2: 例「Technical Learnings: Active Recordアソシエーション逆引き」]
- [アウトプット候補3: 例「週次まとめ（土曜のReflective Output）」]

---

## 6. Sessions DB記録の注意事項

### notesフィールドの構造化

セッション終了時のnotesに以下のタグを使用して記録すること：

```
[Contextual Learning] [学習した技術概念・参照したドキュメント]
[Implementation] [実装作業の内容]
[Outcome] [セッション終了時の成果・状態]
[Friction] [詰まった箇所・課題]
```

**記録例**:
```
[Contextual Learning] buildメソッド（Rails API Dock）、collectionメソッド（Railsガイド）
[Implementation] Tips newアクション、フォームビュー作成
[Outcome] newアクション表示成功、createアクションでスキーマ制約エラー
[Friction] category_id NOT NULL制約の事前確認漏れ
```

### 記録の負荷を減らすコツ

- 完璧を目指さない：3行メモで十分
- セッション終了直後に2分で記録（後回しにしない）
- テンプレートをNotionのデフォルト値として設定

---

## 7. 週末の振り返り指針

週次レビュー作成時に以下を確認：

### 定量評価
- [ ] 週次学習時間 24h以上達成？
- [ ] DS平均 3.3以上達成？
- [ ] 総インプット時間 6h以上達成？（内訳: Focused [X]h, Contextual [X]h, Reflective [X]h）

### 定性評価
- [ ] Learning Density: DS4.0+セッション週3回以上？
- [ ] Conceptual Breakthrough: Insights記述週3個以上？
- [ ] Output-Driven Learning: 技術記事1本 or Technical Learnings更新3回 or 高品質knowledge_organization 2回？

### 実装評価
- [ ] 週次themeで定義された機能の80%以上完了？
- [ ] Top1タスクのDone条件を週5日以上でクリア（部分達成含む）？

### Experiment検証
- [ ] 今週のexperimentは実行されたか？
- [ ] 仮説は検証されたか？成功 or 失敗の判断基準は？
- [ ] 次週に継続 or 修正が必要か？

---

## 付録: 過去の週次戦略との変更点

### v1.0（2026-03-01～03-07）からの主な変更

| 項目 | v1.0 | v2.0（本テンプレート） |
|---|---|---|
| **Reading設計** | 水木でReading切替（強制） | optionalに格下げ、Contextual Learning前提 |
| **Success Criteria** | 「Reading 2h以上」 | 「総インプット時間 6h以上（3分類）」 |
| **新指標** | なし | Learning Density、Conceptual Breakthrough、Output-Driven Learning |
| **daily_top1構造** | 文字列（Done条件のみ） | オブジェクト（Done条件 + expected_contextual_learning） |
| **Shift日設計** | Reading強制 | 技術記事執筆 or 実装継続（optional） |
| **knowledge_organization** | 夜間固定枠あり | 2段階設計（夜は事実記録のみ） |

### v2.0の設計思想

1. **実装中心型学習スタイルを公式化**: 「実装をしながら学習」を前提とした指標設計
2. **質的評価を強化**: 時間ベースから質的評価（DS、Insights記録）へシフト
3. **柔軟性の向上**: optional指標を増やし、「Reading未達 = 失敗」という認識を除去
4. **メタ認知の促進**: Conceptual Breakthrough記録により、学習の言語化を習慣化

---

**このテンプレートは今後の週次戦略作成時に使用すること。過去の戦略は参考にするが、v2.0フォーマットに移行する。**
