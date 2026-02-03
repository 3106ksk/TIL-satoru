# Daily Review: Operation Rules (v2.1)

## 1. 運用フロー概要

| Step | アクション | ツール | 実施タイミング |
| --- | --- | --- | --- |
| **1** | **Record** (記録) | Notion | 学習終了後 (夜) |
| **2** | **Export** (出力) | Notion → Local | 記録完了直後 |
| **3** | **Edit** (整形) | Markdown Editor / Antigravity | 出力後 |
| **3.5** | **QC** (品質チェック) | Antigravity | 整形直後 |
| **4** | **Share** (共有) | Mattermost | 編集完了後 |

## 2. 詳細プロセス

### Step 1: Notion記録 (Record)
- NotionのDailyページに入力。
- **必須**: `Day Mode`, `Top1`, `Done条件`。
- **振り返り**: `Worked`, `Slipped`, `Insight` を必ず埋める。
- **技術学習**: その日の重要な学びを本文下部に集約する。

### Step 2: Export
- ページ右上の `...` > `Export`。
- **Format**: `Markdown & CSV`
- **Include content**: `Everything`
- ダウンロードしたzipを展開し、mdファイルをローカルへ移動。

### Step 3: Edit (整形)
- **推奨**: Antigravity Skill `format_daily_log` を使用。
- **手動の場合**: `docs/daily_log_golden_rules.md` に従いノイズ除去と整形。
- **ファイル名**: `daily_YYYY-MM-DD.md`
- **保存先**: `daily/`

### Step 3.5: QC (品質チェック)
- Antigravity Skill `daily_log_qc` を使用。
- `docs/daily_log_golden_rules.md` のQuality Gateを満たすこと。

### Step 4: Share
- 整形後の内容をMattermostへ投稿。
- 確認:
  - ファイル名は正しいか？
  - 不要なリンクは消えたか？
  - コードブロックは正しいか？

## 3. チェックリスト (Manual)
- [ ] Notionエクスポートを `Markdown & CSV` で実行した
- [ ] ファイル名を `daily_YYYY-MM-DD.md` に変更した
- [ ] `docs/daily_log_golden_rules.md` に従って整形した
  - [ ] Statsプロパティのみ残した
  - [ ] 不要なリンク・メタデータを削除した
  - [ ] 見出しレベル (H1, H2, H3) を修正した
- [ ] `daily_log_qc` の指摘がゼロである
- [ ] Mattermostに投稿した
