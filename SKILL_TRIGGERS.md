# 🤖 AI Agent スキル実行トリガー一覧

このディレクトリ (`.agent/skills/`) に登録されている各スキルを呼び出す（実行させる）ための想定フレーズ（トリガー）と処理内容の概要です。毎日の学習記録や週次レビュー、レポート作成などを自動化する際に参考にしてください。

---

## 📅 日々の記録・計画 (Daily)

### `generate_daily_plan`
**📝 処理内容**: 週次戦略と前日の学習記録を参照して、翌日（または当日）の学習計画（Daily Plan）を自動生成します。
**🗣️ トリガー（呼び出し言葉）**:
- 「明日の学習計画を作成して」
- 「daily planを生成して」
- 「〇月〇日の目標を作成して」
- 「今日の学習目標を作って」

### `format_daily_log`
**📝 処理内容**: Notionの生データとSessions CSVから、最新フォーマット（Fact+Why形式、AI分析フィードバック付き）のDaily Reviewファイルを生成します。
**🗣️ トリガー（呼び出し言葉）**:
- 「Daily Reviewフォーマットを作成して」
- 「日報をフォーマットして」
- 「今日のログを整形して」

### `daily_log_qc`
**📝 処理内容**: 作成したDaily Reviewファイルが最新のフォーマット（Fact+Why形式）に準拠しているか検証し、不備があれば修正提案をします。
**🗣️ トリガー（呼び出し言葉）**:
- 「Daily Reviewを検証して」
- 「今日のログのフォーマットをチェックして」

### `generate-runteq-report`
**📝 処理内容**: 詳細な学習記録（Daily Review）から特定のエッセンスを抽出し、Runteq提出用の簡潔な日誌フォーマットを自動生成します。
**🗣️ トリガー（呼び出し言葉）**:
- 「日誌を作成して」
- 「Runteq日誌を作成して」
- 「daily reportを生成して」

---

## 🗓️ 週次の振り返り・戦略 (Weekly)

### `import_weekly_review`
**📝 処理内容**: Notionからエクスポートされた最新の「Weekly Review (CSV)」を自動検出し、今週分のデータをMarkdownに変換してweeklyフォルダに保存・整理します。
**🗣️ トリガー（呼び出し言葉）**:
- 「Weekly Reviewをインポートして」
- 「週次レビューを取り込んで」

### `weekly_planning_assistant`
**📝 処理内容**: Weekly Strategy（週次戦略）の入力内容を分析し、JSONデータやRisk Assessmentデータを生成、Weekly Reviewファイルにチェックポイントを更新します。
**🗣️ トリガー（呼び出し言葉）**:
- 「週次戦略をプランニングして」
- 「Weekly Strategyを整理して」

### `create_community_report`
**📝 処理内容**: 週次戦略のJSONデータとRisk AssessmentのMarkdownをもとに、特定のフォーマット・トーンでコミュニティ報告用のウィークリーレポートを生成します。
**🗣️ トリガー（呼び出し言葉）**:
- 「コミュニティレポートを作成して」
- 「今週のコミュニティ報告を作って」

---

## 🛠️ データ処理・正規化・整理

### `process_sessions_db_export`
**📝 処理内容**: `daily_sessions_record/` 内の日別セッションファイル（`sessions_YYYY-MM-DD.md`）を指定日付範囲で結合し、`Sessions/Sessions_DB_YYYY-MM-DD_to_YYYY-MM-DD.md` を生成します。`merge_daily_sessions.py` が時刻形式変換・Notes再構造化・WeekKey算出を自動処理します。

**🗣️ トリガー（呼び出し言葉）**:
- 「日別セッションを結合して」
- 「daily_sessions_recordをまとめて」
- 「SessionログをMarkdownに変換して」
- 「Sessions DBを生成して」

### `normalize_learning_log`
**📝 処理内容**: `process_sessions_db_export` で生成した Sessions_DB MD と `daily/` の Daily Review MD を結合して、週次分析用の正規化JSONデータを自動生成します。

**🗣️ トリガー（呼び出し言葉）**:
- 「1週間のログを正規化して」
- 「学習ログを正規化して」
- 「ログから分析用JSONデータを生成して」

### `organize_interview_transcript`
**📝 処理内容**: 面接などの文字起こしファイル（transcript）を読み込み、内容と作成日に基づいて適切なファイル名に変更・整理します。
**🗣️ トリガー（呼び出し言葉）**:
- 「面接の文字起こしを整理して」
- 「transcriptのリネームと移動をお願い」

---

## 🔧 システム・その他

### `skill-creator-best`
**📝 処理内容**: 新しいスキルの作成、または既存スキルのアップデートを行うためのガイドです。Claudeの機能を専門的な知識やワークフローで拡張する際に使用します。
**🗣️ トリガー（呼び出し言葉）**:
- 「新しいスキルを作成して」
- 「〇〇をするためのスキルを作りたい」
- 「既存のスキルをアップデートして」
