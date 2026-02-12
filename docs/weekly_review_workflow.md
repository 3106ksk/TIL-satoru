# Weekly Review Workflow

このドキュメントでは、毎週末に行う学習の振り返り（Weekly Review）の手順をまとめます。

## 事前準備

以下のデータが揃っていることを確認してください：

1.  **Notionデータのエクスポート**:
    *   「Weekly Review」データベース（CSV）
    *   「Sessions」データベース（CSV）
    *   エクスポート先: `notion_exports/`
2.  **Daily Review**:
    *   その週の `daily/daily_YYYY-MM-DD.md` が全て揃っていること。
3.  **今週の戦略ファイル**:
    *   `weekly_strategies/YYYY-MM-DD_to_YYYY-MM-DD.json`
    *   `risk_assessments/YYYY-MM-DD.md`

## ワークフロー詳細

### Step 1: データのインポートと正規化

Notionからエクスポートしたデータを処理し、分析用データを準備します。

1.  **Weekly Review のインポート**:
    *   スキル: `import_weekly_review`
    *   実行コマンド: `python3 .agent/skills/import_weekly_review/scripts/process_weekly_export.py`
    *   成果物: `weekly/weekly_YYYY-MM-DD_to_YYYY-MM-DD.md`
    *   機能: 週次レビューCSVをMarkdownに変換し、`weekly/`フォルダに保存します。

2.  **学習ログの正規化**:
    *   スキル: `normalize_learning_log`
    *   実行コマンド:
        `python3 .agent/skills/normalize_learning_log/scripts/normalize.py`
        または、AIへ指示: 「学習ログを正規化して」
    *   成果物: `normalized_data/normalized_data_YYYY-MM-DD_to_YYYY-MM-DD.json`
    *   機能: Sessions CSVとDaily Markdownを結合し、分析可能なJSON形式に変換します。

### Step 2: 実績分析 (AI Analysis)

正規化されたデータを用いて、今週の学習実績を分析します。

1.  **分析プロンプトの実行**:
    *   使用ファイル: `prompts/weekend_review_prompt.md`
    *   入力: `normalized_data` のJSONファイルの内容
    *   目的: 学習実績の配分（カリキュラム:技術面談:技術書読書 = 6:3:1）との乖離を確認し、次週の調整案を策定します。

### Step 3: レポート作成

分析結果と戦略ファイルを元に、コミュニティへの報告レポートを作成します。

1.  **Community Report の生成**:
    *   スキル: `create_community_report`
    *   指示: "Create a community report for the week of [Date]."
    *   成果物: `community_reports/YYYY-MM-DD_to_YYYY-MM-DD_report.md`
    *   機能: 現在の戦略ファイルとリスク評価MDを読み込み、指定のフォーマットでレポートの下書きを作成します。分析結果（Step 2）の内容を「先週の振り返り」セクションに追記してください。

### Step 4: 次週の計画策定

1.  **次週の戦略作成**:
    *   `weekly_strategies/` に新しいJSONファイルを作成（例: `YYYY-MM-DD_to_YYYY-MM-DD.json`）。
    *   テーマ、目標時間、重点実験（The One Thing）を定義。
    *   `risk_assessments/` に新しいMarkdownファイルを作成し、リスク対策（If-Thenプラン）を記述。

### Step 5: ファイル整理（6週間ごと）

1.  **セットへのアーカイブ**:
    *   6週間（1セット）が終了したら、該当期間のファイルを `sets/YYYY-MM-DD_to_YYYY-MM-DD/` に移動してアーカイブします。
    *   対象フォルダ: `daily/`, `weekly/`, `Sessions/`, `weekly_reviews/`
    *   参照: `AGENTS.md` の「セット管理」ルール
