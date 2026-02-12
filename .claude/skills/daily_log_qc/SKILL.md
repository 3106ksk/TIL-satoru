---
name: daily_log_qc
description: Daily Reviewファイルを最新フォーマット（v2: Fact+Why形式）に準拠しているか検証し、不備があれば修正提案する。
---

# Daily Log Quality Checker Skill (v2)

Daily Reviewファイルが最新フォーマットに準拠しているか検証する。

## 検証対象フォーマット

`.claude/format_daily_log/SKILL.md` で定義された構成に準拠しているかを確認する。

## チェック項目

### 1. 構造チェック

- [ ] H1タイトル: `# YYYY-MM-DD`（`Daily Review` 等の接尾辞なし）
- [ ] 必須セクション（すべて `## ■` 形式）:
  - `## ■ Stats`
  - `## ■ Top1 / Done条件 達成度フィードバック`
  - `## ■ 時間配分フィードバック`
  - `## ■ Worked`
  - `## ■ Slipped`
  - `## ■ Insights`
  - `## ■ Study Strategy for Next Day`
  - `## ■ Technical Learnings`

### 2. Stats セクション

- [ ] 必須フィールド: Day Mode, Budget, Total Min, 純粋な学習時間, 休憩時間, 運動時間, Avg Deep Score, Top1, Done条件
- [ ] Day Mode の値: `OFF（学習日）` または `Shift（ON）`
- [ ] 数値フィールドに `min` 単位が付いているか
- [ ] 純粋な学習時間 + 休憩時間 + 運動時間 ≒ Total Min（誤差許容）

### 3. AI生成フィードバックセクション

- [ ] `■ Top1 / Done条件 達成度フィードバック` に `[定量面]` と `[定性面]` の両方があるか
- [ ] `■ 時間配分フィードバック` に `[定量面]` と `[定性面]` の両方があるか
- [ ] 定量面に具体的な数値（min, %, 件数等）が含まれているか

### 4. Fact + Why 形式チェック（Worked / Slipped / Insights）

- [ ] 各項目が `**Fact**:` + `**Why**:` の2行ペアになっているか
- [ ] Fact行が客観的事実（セッションデータで裏取り可能な内容）か
- [ ] Why行が原因・メカニズムの説明か（Factと重複していないか）
- [ ] 1セクション3項目（6行）以内か
- [ ] プレースホルダー（`[長時間学習を維持できた工夫...]` 等）が残っていないか

### 5. Study Strategy / Technical Learnings

- [ ] Study Strategy for Next Day が存在し、少なくとも1項目あるか
- [ ] Technical Learnings の各トピックが番号付きで分離されているか
- [ ] コードブロックに言語識別子が付いているか

### 6. ノイズチェック

- [ ] Notionリンク（`Untitled`, `https://www.notion.so/...`）が残っていないか
- [ ] メタデータ行（Created time, WeekKey, In This Week 等）が残っていないか

## 出力

- 問題あり: 各問題を行番号付きでリストし、修正案を提示
- 問題なし: 「QC passed: 全項目準拠」と明示

## 参照

- `.claude/format_daily_log/SKILL.md`: 最新フォーマット定義
- `plans/compiled-swimming-kitten.md`: 設計経緯と整形ルールの正
