# Daily Review: Golden Rules (v2.1)

## 1. 目的
AI分析の品質を最大化するため、「情報の重複（ノイズ）」を排除し、「記述のブレ」をなくした標準フォーマットを定義する。

## 2. コア原則（AI向け）
1. **Single Source of Truth**: 数値や結論は“1箇所だけ”に置く（Statsの数値を他セクションで言い直さない）。
2. **Atomic Bullet**: 1行=1事実/1学び。長文・複合文を避ける。
3. **Controlled Vocabulary**: 見出し・ラベル・表現は固定語彙を使う（勝手な言い換え禁止）。
4. **Fact → Reason/Trigger → Next**: 事実と理由/トリガー、次の一手を同一行で明確に分ける。

## 3. ファイル形式と命名
- **拡張子**: `.md` (Markdown)
- **命名規則**: `daily_YYYY-MM-DD.md`
  - 例: `daily_2026-01-27.md`
- **保存場所**: `daily/` ディレクトリ（AGENTS.md参照）

## 4. 黄金の構成（The Golden Structure）
以下の構成と順序を厳守すること。

```markdown
# YYYY-MM-DD Daily Review

■ Stats
- **Day Mode**: Off (OFF) / Shift (ON)
- **Total Min**: [数値] min
- **Deep Score**: [数値]
- **Top1**: [目標内容]

■ Context & Reflection
**Worked**
- 事実: [内容] / 理由: [要因]

**Slipped**
- 事実: [内容] / トリガー: [要因]

**Insight**
- 事実: [内容] / 次の一手: [教訓・行動]

■ Technical Learnings

**1. [領域]: [具体的トピック/エラー名]**
- **Issue**: [何が起きたか] (トラブルシューティング時)
- **Question**: [疑問] (学習・理解時)
- **Cause**: [原因] (任意)
- **Solution/Hypothesis**: [解決策/仮説] (Issue対)
- **Conclusion**: [結論・学び] (Question対)
- **Evidence**: [根拠/結果] (任意)
- **Code**:
  ```lang
  # 必要に応じてコードブロック
  ```
```

## 5. 正規化ルール（Normalization）
- **日付**: H1は必ず `YYYY-MM-DD`（ISO形式）。
- **Day Mode**: 値は `Off (OFF)` か `Shift (ON)` のみ。
- **Total Min**: 整数、単位は `min` 固定。
- **Deep Score**: 小数1桁を推奨（例: `2.8`）。
- **Top1**: 1行1目標。文末の句点は不要。
- **Reflection**: 事実/理由(トリガー)/次の一手のラベルを固定。
- **Technical Learnings**: トピック見出しは `領域: 具体` 形式で統一。
- **Research Stock**: 未解決の疑問は `### 📥 Research Stock` (または `### 未解決`) 以下に箇条書きにする。これらは自動的に `research_stock.md` に移動され、日報からは削除される。

## 6. クリーニングルール（Noise Reduction）
Notionエクスポートに含まれる以下は必ず削除する。

### 削除対象
1. **不要なメタデータ**: `Created time`, `Tags`, `Big Question` などStats以外のプロパティ。
2. **Notion固有リンク**: `Untitled` リレーションリンク、`Sessions DB` のリンク羅列。
3. **空のテンプレ項目**: 未記入のセクションは削除。ただし `Worked/Slipped/Insight` は必ず埋める。

## 7. 重複・ブレ抑制ルール
- **Statsの再掲禁止**: 数値・Top1はStats以外に書かない。
- **同一内容の重複禁止**: Worked/Slipped/Insightで同内容を繰り返さない。
- **学びは1箇所**: Technical Learningsに集約し、他セクションで言い直さない。
- **語彙固定**: 見出しやラベルの表記揺れを許可しない。

## 8. Quality Gate（投稿前チェック）
- [ ] H1/H2/H3の順序と表記がテンプレ通り
- [ ] Statsの4項目が全て埋まっている
- [ ] Worked/Slipped/Insightが全て埋まっている
- [ ] Notion由来のリンク・メタデータが消えている
- [ ] Technical Learningsが「領域: 具体」形式で書かれている
