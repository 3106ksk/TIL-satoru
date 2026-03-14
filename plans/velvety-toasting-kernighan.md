# Plan: format_daily_log スキルに開発ログ同時生成機能を追加

## Context

現在の `format_daily_log` スキルは `daily/daily_YYYY-MM-DD.md` のみを出力する。
ユーザーはアプリ開発の進捗とTechnical LearningsをMattermost（Markdown対応チャットプラットフォーム）で共有したい。
既存スキルのフローに1ステップ追加し、daily整形と同時に `daily_reports/` へ共有用の開発ログも生成する。

## 変更対象ファイル

- `.claude/skills/format_daily_log/SKILL.md` — メイン変更箇所

## 変更内容

### 1. SKILL.md に Step 6 を追加: 開発ログ生成

現在の処理フローは Step 1〜5（データ読み込み → AI分析 → Worked/Slipped整形 → Technical Learnings構造化 → ファイル出力）。
ここに **Step 6: 開発ログ生成** を追加する。

#### Step 6 の処理内容

**抽出対象（生データの `📝 Context & Reflection` セクションから）:**
1. **開発進捗**: 「アプリ開発N日目」で始まるブロック（実装内容のリスト含む）
2. **学習の気づき**: 「実装前に〜」のような実装プロセスに関するメタ認知的記述
3. **Technical Learnings**: Q&A形式の技術的学び（コードブロック含む）

**抽出ルール:**
- 生データの `📝 Context & Reflection` 内に、見出しまたは先頭行として `アプリ開発N日目`（Nは整数）が存在する場合のみ生成
- `実装` / `開発` などの単一キーワード一致だけでは生成しない
- `アプリ開発N日目` が存在しない場合は Step 6 をスキップ（開発ログは生成しない）
- Step 6 スキップ時に同日 `daily_reports/dev_log_YYYY-MM-DD.md` が既に存在する場合は削除し、再実行結果と整合させる
- Technical Learnings は Step 4 で構造化済みのものを再利用

#### 出力フォーマット（Mattermost向けMarkdown）

```markdown
# 開発ログ YYYY-MM-DD

## 今日の進捗

{開発進捗の記述をそのまま転記。箇条書き構造は保持}

## 気づき・所感

{実装プロセスに関するメタ認知的記述を転記}

## Technical Learnings

### Q: {疑問}
**A:** {回答・結論}

{コードブロックがあればそのまま含める}

### Q: {疑問2}
**A:** {回答2}

---
参照: {参照URLがあれば記載}
```

**フォーマット設計の根拠:**
- Mattermostは `###` まで見出し対応、コードブロック・テーブルも対応
- Q&A形式は `### Q:` + `**A:**` で視認性を確保
- 長いコード例はコードブロックで折りたたみなしでそのまま掲載（Mattermostの仕様）

#### 出力先

- `daily_reports/dev_log_YYYY-MM-DD.md`
- 命名規則: `generate-runteq-report` の `daily_report_` と区別するため `dev_log_` プレフィックスを使用

### 2. SKILL.md の冒頭descriptionを更新

```
description: Notion生データ + Sessions CSVから、最新フォーマットのdailyログを生成する。
Fact+Why形式、AI分析フィードバック付き。開発ログがある日は共有用の開発ログも同時生成。
```

### 3. 検証チェックリストに追加

既存チェックリストの末尾に:
- [ ] 開発ログ該当日の場合、`daily_reports/dev_log_YYYY-MM-DD.md` が生成されているか
- [ ] Technical Learningsの内容がdaily出力と開発ログ出力で一致しているか
- [ ] 開発ログ非該当日の場合、`daily_reports/dev_log_YYYY-MM-DD.md` が生成されないこと（既存があれば削除されること）

## 変更しないもの

- Step 1〜5 の既存ロジック（一切変更なし）
- `generate-runteq-report` スキル（別用途、関係なし）
- ディレクトリ構成（`daily_reports/` は既存）

## 検証方法

1. 今回の 2026-03-02 のデータで `format_daily_log` を実行
2. `daily/daily_2026-03-02.md` が従来通り生成されることを確認
3. `daily_reports/dev_log_2026-03-02.md` が同時に生成されることを確認
4. dev_log のMarkdownをMattermostにペーストして表示崩れがないことを目視確認
5. `アプリ開発N日目` を含まない日のデータで実行し、`daily_reports/dev_log_YYYY-MM-DD.md` が生成されないことを確認
