# リポジトリ構成リファクタリング計画

## Context

**リポジトリの主目的**: RUNTEQ受講生としてのWeb開発学習を、メトリクスベース（Deep Score、Cognitive Headroom等）で科学的に管理する**構造化された学習記録・成長管理システム**。

**現状の問題**:
- ルートに16個のファイルが散乱（技術メモ、プロンプト、ドラフト、空ファイルが混在）
- `.gitignore` が存在せず `.DS_Store` がgit管理されている
- ファイル命名が不統一（日本語/英語混在、スペース入り、typo）
- `notion_exports/` にzip・CSV・MDが未整理で混在
- `docs/` に2ファイルしかなく、本来そこに属すべきファイルがルートに散乱
- `prompts/` も同様に1ファイルのみ
- `technical_interviews/` 内に性質の異なるファイルが重複

---

## 推奨ディレクトリ構造

```
/学習アウトプット/
├── .agent/skills/                    # [変更なし] Agent用スキル定義（存在する場合）
├── .gitignore                        # [新規]
├── AGENTS.md                         # [更新] 命名規則を拡張
├── README.md                         # [更新] 構造説明を充実化
│
│  ── アクティブ期間データ（AGENTS.md セット管理対象）──
├── daily/                            # 日次学習ログ
├── Sessions/                         # セッション記録
├── weekly/                           # 週次ログ
├── weekly_strategies/                # 週計画
├── weekly_reviews/                   # 週次レビュー（年フォルダ配下）
├── sets/                             # 6週間セットアーカイブ
│
│  ── ナレッジ蓄積（恒久、セット管理対象外）──
├── docs/                             # 方法論・ガイドライン（人間が参照する恒久文書）
├── notes/                            # [新規] 技術メモ（技術カテゴリ別サブディレクトリ）
│   ├── rails/
│   ├── javascript/
│   └── ideas/
├── prompts/                          # AIプロンプトテンプレート
├── technical_interviews/             # 技術面談（エントリDB + トランスクリプト）
│   └── transcripts/
│
│  ── Agent生成物 ──
├── normalized_data/                  # 正規化済みJSON
├── community_reports/                # コミュニティレポート
├── risk_assessments/                 # リスク評価
├── outputs/                          # その他成果物・レポート
│
│  ── 一時領域 ──
├── notion_exports/                   # Notionエクスポート一時置き場
└── plans/                            # Agent計画ファイル
```

---

## ルート散乱ファイルの移動先

| 現在のファイル | 移動先 | 操作 |
|---|---|---|
| `leaning-framework.md` | `docs/learning_framework.md` | typo修正 + 移動 |
| `runteq_engineer_skills.md` | `docs/runteq_engineer_skills.md` | 移動 |
| `share.md` | `docs/debug_verbalization_template.md` | 意味のある名前に変更 + 移動 |
| `reflection_list.md` | `docs/reflection_metrics.md` | リネーム + 移動 |
| `ai-question-format.md` | `prompts/ai_question_format.md` | 命名統一 + 移動 |
| `weekend_promptv3.md` | `prompts/weekend_review_prompt.md` | バージョン番号除去 + 移動 |
| `week stra.md` | `prompts/weekly_strategy_prompt.md` | スペース除去・正式名称化 + 移動 |
| `rails_mount_engine_routing.md` | `notes/rails/mount_engine_routing.md` | 移動 |
| `ActiveRecord RecordNotFound...md` | `notes/rails/activerecord_record_not_found.md` | 正規化 + 移動 |
| `promise_tutorial_md.md` | `notes/javascript/promise_tutorial.md` | リネーム + 移動 |
| `時間割アプリ相談.md` | `notes/ideas/timetable_app_consultation.md` | 英語名に統一 + 移動 |
| `test-script.md` | `notes/ideas/agent_skill_design_memo.md` | 内容反映した名前 + 移動 |
| `project_progress_report.md` | `outputs/project_progress_report.md` | 移動 |
| `learning-output_01_31.md` | `outputs/learning_output_YYYY-MM-DD.md` | 本文から日付抽出して統一 + 移動 |
| `learning_log.ics` | `outputs/learning_log.ics` | 移動 |
| `my_shchdule.md` | (削除) | 空ファイル・typo |
| `research_stock.md` | ルートに残す | **確定: アクセス頻度が高いため** |

### technical_interviews/ の整理
- `technical_interviews.md`（面談エントリDB）→ そのまま維持（リネーム: `entries.md`）
- `技術面談.md`（実装プロセスの方法論サマリー）→ `docs/implementation_process_guide.md` に移動

### その他リネーム
- `weekly_strategies/Weekly Strategy Design.md` → `weekly_strategies/weekly_strategy_design.md`

---

## .gitignore（新規作成）

```gitignore
# macOS
.DS_Store
**/.DS_Store

# Notion exports (binary artifacts)
notion_exports/*.zip
notion_exports/ExportBlock-*/

# Editor & IDE
*.swp
*.swo
*~
.vscode/
.idea/

# plans/ は計画ファイルを追跡するなら除外しない
```

既にトラッキング中の `.DS_Store` は `git rm --cached` で追跡除去する。

---

## 命名規則

1. **英語・小文字・アンダースコア区切り**（`daily_log_golden_rules.md`）
2. **日付は `YYYY-MM-DD`**（ISO 8601）
3. **バージョン番号はファイル名に含めない**（gitで管理）
4. **スペース禁止**
5. **ファイル名から内容が推測可能であること**

---

## 移行手順

### Step 0: 事前確認
- `git status` でGit管理されているかと作業ツリーの状態を確認
- 現在のブランチ名（`main` かどうか）を確認

### Step 1: 安全確保
- 未コミット変更をコミット
- `git branch backup/pre-restructure` でバックアップ
- `git checkout -b refactor/repository-structure`

### Step 2: .gitignore 追加 + .DS_Store 除去
- `.gitignore` 作成
- `git rm --cached` で全 `.DS_Store` を追跡除去
- コミット

### Step 3: 空ファイル削除
- `my_shchdule.md` 削除
- コミット

### Step 4: docs/ へ移動（方法論・ガイドライン）
- `leaning-framework.md` → `docs/learning_framework.md`
- `runteq_engineer_skills.md` → `docs/`
- `share.md` → `docs/debug_verbalization_template.md`
- `reflection_list.md` → `docs/reflection_metrics.md`
- `技術面談.md` → `docs/implementation_process_guide.md`
- コミット

### Step 5: prompts/ へ移動
- `ai-question-format.md`, `weekend_promptv3.md`, `week stra.md` → `prompts/`
- コミット

### Step 6: notes/ 作成 + 技術メモ移動
- `mkdir -p notes/rails notes/javascript notes/ideas`
- 技術メモ5ファイルを移動
- コミット

### Step 7: outputs/ へ移動
- `project_progress_report.md`, `learning-output_01_31.md`, `learning_log.ics` → `outputs/`
- コミット

### Step 8: technical_interviews/ 整理
- `technical_interviews.md` → `entries.md` にリネーム
- コミット

### Step 9: リネーム（命名規則統一）
- `Weekly Strategy Design.md` → `weekly_strategy_design.md`
- コミット

### Step 10: README.md 更新
- リポジトリ目的、構造説明、ファイル配置フローを記述
- コミット

### Step 11: AGENTS.md 更新
- `notes/`, `prompts/`, `docs/` の命名規則を追記
- 「新規ファイルをどこに置くか」判定フローを追記
- コミット

### Step 12: マージ・検証
- ルートに残るのは `AGENTS.md`, `README.md`, `.gitignore`, `research_stock.md` のみか確認
- `main` にマージ

---

## 検証方法

1. `ls` でルートディレクトリにファイルが散乱していないことを確認
2. `git status` でuntracked/modifiedファイルがないことを確認
3. 各ディレクトリ内のファイルが命名規則に準拠していることを確認
4. `.DS_Store` がgit管理から除外されていることを `git ls-files` で確認
5. `AGENTS.md` のセット管理ルールが既存データと整合していることを確認
