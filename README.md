# 学習アウトプット

## リポジトリの目的

RUNTEQ受講生としてのWeb開発学習を、メトリクスベース（Deep Score、Cognitive Headroom等）で科学的に管理する**構造化された学習記録・成長管理システム**。

## ディレクトリ構造

```
/学習アウトプット/
├── .agent/skills/              # Agent用スキル定義
├── .gitignore                  # Git除外設定
├── AGENTS.md                   # Agent動作ルール・命名規則
├── README.md                   # このファイル
│
│  ── アクティブ期間データ（AGENTS.md セット管理対象）──
├── daily/                      # 日次学習ログ
├── Sessions/                   # セッション記録
├── weekly/                     # 週次ログ
├── weekly_strategies/          # 週計画
├── sets/                       # 6週間セットアーカイブ
│
│  ── ナレッジ蓄積（恒久、セット管理対象外）──
├── docs/                       # 方法論・ガイドライン（人間が参照する恒久文書）
├── notes/                      # 技術メモ（技術カテゴリ別サブディレクトリ）
│   ├── rails/
│   ├── javascript/
│   └── ideas/
├── prompts/                    # AIプロンプトテンプレート
├── technical_interviews/       # 技術面談（エントリDB + トランスクリプト）
│   └── transcripts/
│
│  ── Agent生成物 ──
├── normalized_data/            # 正規化済みJSON
├── community_reports/          # コミュニティレポート
├── risk_assessments/           # リスク評価
├── outputs/                    # その他成果物・レポート
│
│  ── 一時領域 ──
├── notion_exports/             # Notionエクスポート一時置き場
└── plans/                      # Agent計画ファイル
```

## 命名規則

1. **英語・小文字・アンダースコア区切り**（例: `daily_log_golden_rules.md`）
2. **日付は `YYYY-MM-DD`**（ISO 8601形式）
3. **バージョン番号はファイル名に含めない**（gitで管理）
4. **スペース禁止**
5. **ファイル名から内容が推測可能であること**

## ファイル配置フロー

- **学習ログ**: `daily/`, `weekly/`, `Sessions/` に配置
- **計画**: `weekly_strategies/` に配置
- **方法論・ガイドライン**: `docs/` に配置
- **技術メモ**: `notes/<category>/` に配置（category: rails, javascript, ideas等）
- **プロンプト**: `prompts/` に配置
- **成果物・レポート**: `outputs/` に配置
- **Notionエクスポート**: `notion_exports/` に一時配置（.gitignoreで除外）

詳細は [AGENTS.md](AGENTS.md) を参照。
