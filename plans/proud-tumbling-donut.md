# Plan: `extract_daily_sessions` スキル作成

## Context

Sessions CSVから1日分のセッションレコードを抽出し、サマリー付き構造化Markdownを生成するスキル。
既存の`process_sessions_db_export`が**週単位の生データアーカイブ**であるのに対し、本スキルは**日単位の人間向けレポート**を生成する。出力は`format_daily_log`の参照データとしても活用される。

## 作成ファイル（3つ）

| # | パス | 内容 |
|---|------|------|
| 1 | `.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py` | Python3 抽出スクリプト |
| 2 | `.claude/skills/extract_daily_sessions/SKILL.md` | スキル定義 |
| 3 | `CLAUDE.md`（既存ファイル編集） | Skills セクションにエントリ追加 |

## 1. Python スクリプト設計

**CLI**: `python3 extract_daily_sessions.py <input_csv> <target_date> <output_dir>`

**出力**: `<output_dir>/sessions_YYYY-MM-DD.md`

### 処理フロー
1. CSV読み込み（BOM対応、`csv.reader`で複数行Notesも正しく処理）
2. カラム名でインデックス検出（カラム順序が異なるCSVバリアントに対応）
3. Date列で対象日のレコードをフィルタ → start time昇順ソート
4. サマリー計算（総セッション数、総時間、Deep Flag数、平均Deep Score ※Rest/Exercise除外）
5. タイムスタンプ解析（`"March 3, 2026 7:29 AM (GMT+9)"` → `"7:29"`）※`normalize.py`のパターン流用
6. Notes解析（`やった：` / `詰まった/気づいた：` を分離）
7. Markdown生成 → ファイル出力

### 出力フォーマット（プロトタイプ `sessions_2026-03-03.md` に準拠）
```
# Sessions Record: YYYY-MM-DD (Week YYYY-W##)
## Summary    — メトリクステーブル
## Sessions   — 10カラムの一覧テーブル
## Notes      — セッションごとの やった/詰まった・気づいた
```

### エラーハンドリング
- CSV未発見 / 空ファイル / 必須カラム欠落 → エラー終了
- 対象日のレコード0件 → 警告表示、"No sessions recorded" の最小MDを生成（exit 0）
- タイムスタンプ/数値パース失敗 → 警告出力、`-` で代替

## 2. SKILL.md

既存スキルのフォーマットに準拠：
- YAML frontmatter: `name`, `description`
- Usage / Instructions for Agent / Prerequisites / Example
- `format_daily_log`との連携について記載

## 3. CLAUDE.md 更新

Skills セクション（`process_sessions_db_export`の前あたり）に追加：
```markdown
### extract_daily_sessions — Daily Sessions 抽出
- **発火条件**: 「セッション記録を抽出して」「今日のセッションを出力して」等の指示
- **入力**: `notion_exports/` 内のSessions DB CSV + 対象日付
- **出力**: `daily_sessions_record/sessions_YYYY-MM-DD.md`
- **スクリプト**: `.claude/skills/extract_daily_sessions/scripts/extract_daily_sessions.py`
- **参照**: `.claude/skills/extract_daily_sessions/SKILL.md`
```

## 検証手順

1. 既存CSV + 日付 `2026-03-03` でスクリプト実行
2. 出力がプロトタイプ `daily_sessions_record/sessions_2026-03-03.md` と同等であることを確認
3. 存在しない日付（レコード0件）でエラーなく最小MDが生成されることを確認
