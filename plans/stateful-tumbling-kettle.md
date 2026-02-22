# プロジェクト分離計画：学習ログ分析 vs 学習ナレッジベース

## Context

現在の「学習アウトプット」リポジトリは、2つの異なる目的のコンテンツが混在している：

1. **学習ログ分析**（本来の目的）：RUNTEQ学習進捗のメトリクスベース追跡（Deep Score、Cognitive Headroom、Daily/Weekly Review）
2. **学習ナレッジ・記事執筆**：再利用可能な方法論、記事、アプリアイデア、技術メモ

この混在により、以下の問題が発生：
- リポジトリ内のファイル配置が煩雑（31ルートレベル項目）
- RUNTEQ特化コンテンツと汎用コンテンツの境界が不明瞭
- 学習ログ分析に集中しづらい

**解決策**：リポジトリを明確な目的別に分離し、各プロジェクトの焦点を明確化する。

---

## 分離戦略

### プロジェクトA：学習アウトプット（既存、継続）
**目的**：RUNTEQ学習進捗の定量的追跡・分析システム

**スコープ**：
- 時系列学習記録（daily/, weekly/, Sessions/）
- 学習メトリクス（Deep Score、Cognitive Headroom）
- 分析データ（normalized_data/, community_reports/）
- Agent skills（ログ処理・分析自動化）
- 学習ログ特化のワークフロー・プロンプト

---

### プロジェクトB：学習ナレッジベース（新規作成）
**目的**：Web開発の再利用可能なナレッジアセット

**スコープ**：
- 記事・エッセイ（学習方法論、技術ガイド等）
- アプリアイデア・企画書
- 開発方法論・フレームワーク
- 技術メモ（Rails、JavaScript等）
- 汎用プロンプトテンプレート
- 技術面談記録（全件）
- 成果物・レポート（outputs/）

---

## 移行対象ファイル（合計28ファイル + outputs/ディレクトリ）

### 1. 記事・エッセイ（3ファイル）
```
記事.md → articles/mini_app_development_reflection.md
notes/ai_learning_methodology.md → articles/ai_era_learning_theory.md
infrastructure_tips_1.md → guides/infrastructure_tips_for_beginners.md
```

### 2. アプリアイデア（5ファイル + 1削除）
```
notes/app_ideas/learning_tips_consultation.md → app_ideas/learning_tips_consultation.md
notes/app_ideas/gochi_fit.md → app_ideas/gochi_fit.md
notes/app_ideas/reappraisal_app.md → app_ideas/reappraisal_app.md
notes/app_ideas/consultation_tech_research_prompt.md → app_ideas/consultation_tech_research_prompt.md
notes/app_ideas/timetable_app_consultation.md → app_ideas/timetable_app_consultation.md
相談.md → 削除（learning_tips_consultationの下書き、重複）
```

### 3. 汎用方法論・ガイド（6ファイル）
```
docs/app_development_guide.md → guides/app_development_guide.md
docs/mvp_definitions_and_tips.md → guides/mvp_definitions_and_tips.md
docs/learning_framework.md → guides/learning_framework.md
docs/debug_verbalization_template.md → guides/debug_verbalization_template.md
docs/implementation_process_guide.md → guides/implementation_process_guide.md
docs/runteq_engineer_skills.md → guides/runteq_engineer_skills.md
```

### 4. 汎用プロンプト（3ファイル）
```
prompts/tech_selection_pagination.md → prompts/tech_selection_pagination.md
prompts/ai_question_format.md → prompts/ai_question_format.md
prompts/log_reading_practice.md → prompts/log_reading_practice.md
```

### 5. 技術面談（8ファイル、全件移行）
```
technical_interviews/transcripts/2026-02-03_Githubドキュメント読み解き方.md → interviews/github_docs_reading.md
technical_interviews/transcripts/2026-02-05_Rails_CurrentUser_Helper_Method.md → interviews/rails_current_user_helper.md
technical_interviews/transcripts/2026-02-06_Gemドキュメントの読み方.md → interviews/gem_docs_reading.md
technical_interviews/transcripts/2026-02-13_アプリアイデア構築方法.md → interviews/app_idea_construction.md
technical_interviews/transcripts/2026-02-12_ミニアプリ開発と卒業制作の方向性相談.md → interviews/mini_app_and_graduation_direction.md
technical_interviews/transcripts/2026-02-15_ミニアプリ開発の技術選定とAI機能相談.md → interviews/mini_app_tech_selection_and_ai_feature.md
technical_interviews/transcripts/2026-01-15_技術面談6_デバッグの思考プロセスについて.txt → interviews/debugging_thinking_process.txt
technical_interviews/transcripts/2026-01-17_技術面談8_アプリ相談.txt → interviews/app_consultation_session.txt
```

### 6. 技術メモ（3ファイル）
```
notes/rails/activerecord_record_not_found.md → notes/rails/activerecord_record_not_found.md
notes/rails/mount_engine_routing.md → notes/rails/mount_engine_routing.md
notes/javascript/promise_tutorial.md → notes/javascript/promise_tutorial.md
```

### 7. 成果物・レポート（outputs/ 全体）
```
outputs/ → outputs/
（すべてのファイル・サブディレクトリを含む）
```

**合計移行ファイル数**：28ファイル + outputs/ディレクトリ全体

---

## 学習アウトプットに残すファイル

### 学習ログデータ（アクティブ）
- `daily/` - 日次レビュー（35+ファイル）
- `weekly/` - 週次サマリー
- `Sessions/` - セッション記録CSV
- `weekly_reviews/` - 構造化週次レビュー
- `weekly_strategies/` - 週次計画

### 分析・レポート
- `normalized_data/` - 正規化済みJSON
- `community_reports/` - コミュニティレポート
- `risk_assessments/` - リスク評価
- `sets/` - 6週間アーカイブ

### 学習ログ特化ドキュメント（4ファイル残存）
- `docs/daily_log_golden_rules.md`
- `docs/daily_log_operations.md`
- `docs/weekly_review_workflow.md`
- `docs/reflection_metrics.md`

### 学習ログ特化プロンプト（4ファイル残存）
- `prompts/gap_analysis_prompt.md`
- `prompts/weekly_strategy_prompt.md`
- `prompts/weekend_review_prompt.md`
- `prompts/analysis_prompt_v2.md`

### Agentインフラ・その他
- `.agent/skills/` - すべてのスキル
- `.claude/skills/`
- `plans/` - Agent計画ファイル
- `notes/ideas/agent_skill_design_memo.md` - 学習システム設計関連
- `notion_exports/` - 一時領域
- `README.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`

---

## 新プロジェクト構造：学習ナレッジベース

```
/学習ナレッジベース/
├── README.md                     # プロジェクト概要
├── .gitignore
│
├── articles/                     # 記事・エッセイ
│   ├── mini_app_development_reflection.md
│   ├── ai_era_learning_theory.md
│   └── ...
│
├── guides/                       # 開発方法論・ガイド
│   ├── app_development_guide.md
│   ├── mvp_definitions_and_tips.md
│   ├── learning_framework.md
│   ├── debug_verbalization_template.md
│   ├── implementation_process_guide.md
│   ├── runteq_engineer_skills.md
│   └── infrastructure_tips_for_beginners.md
│
├── app_ideas/                    # プロジェクト企画
│   ├── learning_tips_consultation.md
│   ├── gochi_fit.md
│   ├── reappraisal_app.md
│   ├── consultation_tech_research_prompt.md
│   └── timetable_app_consultation.md
│
├── prompts/                      # 汎用プロンプトテンプレート
│   ├── tech_selection_pagination.md
│   ├── ai_question_format.md
│   └── log_reading_practice.md
│
├── interviews/                   # 技術面談記録
│   ├── github_docs_reading.md
│   ├── rails_current_user_helper.md
│   ├── gem_docs_reading.md
│   ├── app_idea_construction.md
│   ├── mini_app_and_graduation_direction.md
│   ├── mini_app_tech_selection_and_ai_feature.md
│   ├── debugging_thinking_process.txt
│   └── app_consultation_session.txt
│
├── notes/                        # 技術メモ
│   ├── rails/
│   │   ├── activerecord_record_not_found.md
│   │   └── mount_engine_routing.md
│   └── javascript/
│       └── promise_tutorial.md
│
└── outputs/                      # 成果物・レポート
    ├── project_progress_report.md
    ├── learning_output_2026-01-31.md
    ├── learning_log.ics
    └── 2026-01-31_20-29-04/
        └── slide_handwritten.png
```

---

## 実装手順（3日間、1-2週間移行期間）

### Day 1：新プロジェクト作成とファイルコピー（2-3時間）

#### 1.1 新リポジトリ初期化
```bash
cd ~/Documents
mkdir 学習ナレッジベース
cd 学習ナレッジベース
git init
```

#### 1.2 ディレクトリ構造作成
```bash
mkdir -p articles guides app_ideas prompts interviews notes/rails notes/javascript outputs
```

#### 1.3 README.md作成
```markdown
# 学習ナレッジベース (Learning Knowledge Base)

Web開発の再利用可能なナレッジアセット集。

## 目的

このリポジトリは、プロジェクト横断で利用可能な方法論、技術ガイド、アプリアイデアを蓄積する。

## ディレクトリ構造

- `articles/` - 記事・エッセイ
- `guides/` - 開発方法論・ガイド
- `app_ideas/` - プロジェクト企画・仕様書
- `prompts/` - 汎用プロンプトテンプレート
- `interviews/` - 技術面談記録
- `notes/` - 技術メモ（カテゴリ別）
- `outputs/` - 成果物・レポート

## 命名規則

1. **英語・小文字・アンダースコア区切り**（例: `app_development_guide.md`）
2. **バージョン番号はファイル名に含めない**（gitで管理）
3. **スペース禁止**
4. **ファイル名から内容が推測可能であること**

## 関連プロジェクト

- [学習アウトプット](../学習アウトプット) - RUNTEQ学習ログ追跡システム
```

#### 1.4 .gitignore作成
```
.DS_Store
*.swp
*.swo
.vscode/
.idea/
Thumbs.db
```

#### 1.5 ファイルコピー（記事・アプリアイデア・ガイド）
```bash
cd ~/Documents/学習アウトプット

# 記事
cp 記事.md ~/Documents/学習ナレッジベース/articles/mini_app_development_reflection.md
cp notes/ai_learning_methodology.md ~/Documents/学習ナレッジベース/articles/ai_era_learning_theory.md
cp infrastructure_tips_1.md ~/Documents/学習ナレッジベース/guides/infrastructure_tips_for_beginners.md

# アプリアイデア
cp notes/app_ideas/learning_tips_consultation.md ~/Documents/学習ナレッジベース/app_ideas/
cp notes/app_ideas/gochi_fit.md ~/Documents/学習ナレッジベース/app_ideas/
cp notes/app_ideas/reappraisal_app.md ~/Documents/学習ナレッジベース/app_ideas/
cp notes/app_ideas/consultation_tech_research_prompt.md ~/Documents/学習ナレッジベース/app_ideas/
cp notes/app_ideas/timetable_app_consultation.md ~/Documents/学習ナレッジベース/app_ideas/

# ガイド
cp docs/app_development_guide.md ~/Documents/学習ナレッジベース/guides/
cp docs/mvp_definitions_and_tips.md ~/Documents/学習ナレッジベース/guides/
cp docs/learning_framework.md ~/Documents/学習ナレッジベース/guides/
cp docs/debug_verbalization_template.md ~/Documents/学習ナレッジベース/guides/
cp docs/implementation_process_guide.md ~/Documents/学習ナレッジベース/guides/
cp docs/runteq_engineer_skills.md ~/Documents/学習ナレッジベース/guides/
```

---

### Day 2：残りファイルコピーと新プロジェクトコミット（2-3時間）

#### 2.1 プロンプト・面談記録・技術メモコピー
```bash
cd ~/Documents/学習アウトプット

# プロンプト
cp prompts/tech_selection_pagination.md ~/Documents/学習ナレッジベース/prompts/
cp prompts/ai_question_format.md ~/Documents/学習ナレッジベース/prompts/
cp prompts/log_reading_practice.md ~/Documents/学習ナレッジベース/prompts/

# 技術面談
cp "technical_interviews/transcripts/2026-02-03_Githubドキュメント読み解き方.md" \
   ~/Documents/学習ナレッジベース/interviews/github_docs_reading.md
cp "technical_interviews/transcripts/2026-02-05_Rails_CurrentUser_Helper_Method.md" \
   ~/Documents/学習ナレッジベース/interviews/rails_current_user_helper.md
cp "technical_interviews/transcripts/2026-02-06_Gemドキュメントの読み方.md" \
   ~/Documents/学習ナレッジベース/interviews/gem_docs_reading.md
cp "technical_interviews/transcripts/2026-02-13_アプリアイデア構築方法.md" \
   ~/Documents/学習ナレッジベース/interviews/app_idea_construction.md
cp "technical_interviews/transcripts/2026-02-12_ミニアプリ開発と卒業制作の方向性相談.md" \
   ~/Documents/学習ナレッジベース/interviews/mini_app_and_graduation_direction.md
cp "technical_interviews/transcripts/2026-02-15_ミニアプリ開発の技術選定とAI機能相談.md" \
   ~/Documents/学習ナレッジベース/interviews/mini_app_tech_selection_and_ai_feature.md
cp "technical_interviews/transcripts/2026-01-15_技術面談6_デバッグの思考プロセスについて.txt" \
   ~/Documents/学習ナレッジベース/interviews/debugging_thinking_process.txt
cp "technical_interviews/transcripts/2026-01-17_技術面談8_アプリ相談.txt" \
   ~/Documents/学習ナレッジベース/interviews/app_consultation_session.txt

# 技術メモ
cp -r notes/rails ~/Documents/学習ナレッジベース/notes/
cp -r notes/javascript ~/Documents/学習ナレッジベース/notes/

# outputs/全体
cp -r outputs/* ~/Documents/学習ナレッジベース/outputs/
```

#### 2.2 新プロジェクトコミット
```bash
cd ~/Documents/学習ナレッジベース
git add .
git commit -m "Initial commit: Web development knowledge base

- Articles: Mini-app development reflection, AI learning theory
- Guides: App development, MVP definitions, learning frameworks (7 guides)
- App Ideas: 5 project specs with consultation notes
- Prompts: 3 general-purpose templates
- Interviews: 8 technical consultation transcripts (all files)
- Notes: Rails (2 files) and JavaScript (1 file) technical memos
- Outputs: All project outputs and reports

Total: 28 files + outputs/ directory migrated from 学習アウトプット repository

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

### 1-2週間移行期間：両プロジェクトで並行運用

**目的**：新プロジェクト構造の検証と問題の早期発見

**運用方針**：
- 新ファイルは「学習ナレッジベース」に直接作成
- 既存ファイルは両方に残存（問題があれば元に戻せる）
- 学習ログ分析のAgent skillsが正常動作することを確認
- ファイル配置基準が明確になっているか検証

**検証項目**：
- [ ] format_daily_log スキル正常動作
- [ ] normalize_learning_log スキル正常動作
- [ ] 新ファイル配置判断が迷いなくできる
- [ ] どちらのプロジェクトを開くべきか即座に判断できる

---

### 移行期間終了後：学習アウトプットからファイル削除（1時間）

#### 削除コマンド
```bash
cd ~/Documents/学習アウトプット

# 記事・ルートファイル
git rm 記事.md infrastructure_tips_1.md 相談.md

# ガイド
git rm docs/app_development_guide.md
git rm docs/mvp_definitions_and_tips.md
git rm docs/learning_framework.md
git rm docs/debug_verbalization_template.md
git rm docs/implementation_process_guide.md
git rm docs/runteq_engineer_skills.md

# プロンプト
git rm prompts/tech_selection_pagination.md
git rm prompts/ai_question_format.md
git rm prompts/log_reading_practice.md

# アプリアイデア
git rm -r notes/app_ideas/

# 技術面談
git rm -r technical_interviews/

# 技術メモ
git rm -r notes/rails/
git rm -r notes/javascript/
git rm notes/ai_learning_methodology.md

# outputs/
git rm -r outputs/
```

#### README.md更新
```markdown
## ディレクトリ構造

├── docs/                       # 学習方法論・ガイドライン（学習ログ特化）
├── notes/ideas/                # 学習システム設計メモ
├── prompts/                    # 学習分析用プロンプト

## 関連プロジェクト

- [学習ナレッジベース](../学習ナレッジベース) - Web開発の再利用可能なナレッジアセット
```

#### AGENTS.md更新（Section 7）
```markdown
### docs/ (方法論・ガイドライン)
- 形式: `docs/<descriptive_name>.md`
- **学習ログ分析に関連する**恒久的な文書のみ
- 例: `daily_log_golden_rules.md`, `reflection_metrics.md`
- 一般的な開発ガイドは「学習ナレッジベース」リポジトリへ

### notes/ (技術メモ)
- 形式: `notes/<category>/<descriptive_name>.md`
- カテゴリ: `ideas/` (学習システム設計関連のみ)
- 一般的な技術メモ（Rails、JavaScript等）は「学習ナレッジベース」リポジトリへ

### outputs/ (成果物・レポート)
- **このディレクトリは削除されました**
- すべての成果物・レポートは「学習ナレッジベース」リポジトリへ移行

### technical_interviews/ (技術面談記録)
- **このディレクトリは削除されました**
- 技術面談記録は全件「学習ナレッジベース」リポジトリへ移行
```

#### クリーンアップコミット
```bash
git add -A
git commit -m "Refactor: Separate general knowledge to new repository

Moved 28 files + outputs/ to '学習ナレッジベース' repository:
- 3 articles/essays
- 6 general methodologies
- 5 app ideas
- 3 general prompts
- 8 technical interviews (all files)
- 3 technical notes (Rails, JavaScript)
- All outputs/

This repository now focuses exclusively on RUNTEQ learning log tracking.

Updated README.md and AGENTS.md to reflect new scope.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## ファイル配置判断基準（今後の参考）

新規ファイル作成時の5つの質問：

1. **RUNTEQ特化コンテンツか？**
   - YES → 学習アウトプット検討
   - NO → 学習ナレッジベース検討

2. **特定の学習期間・日付を含むか？**
   - YES → 学習アウトプット
   - NO → 学習ナレッジベース

3. **Agent skillsや分析で消費されるか？**
   - YES → 学習アウトプット
   - NO → 学習ナレッジベース

4. **プロジェクト横断で再利用可能か？**
   - YES → 学習ナレッジベース
   - NO → 学習アウトプット

5. **学習メトリクスを含むか？**
   - YES → 学習アウトプット
   - NO → 学習ナレッジベース

---

## 成功指標

### 即時（移行完了時）
- [ ] 28ファイル + outputs/ が正常にコピーされている
- [ ] 新プロジェクトがgit管理下にある
- [ ] Agent skills（format_daily_log, normalize_learning_log）が正常動作

### 短期（1-2週間移行期間）
- [ ] 新ファイル配置に迷いがない
- [ ] どちらのプロジェクトを開くべきか即座に判断できる
- [ ] クロスリファレンスの必要性がない（または最小限）

### 長期（1-3ヶ月）
- [ ] ファイル配置ミス率 < 5%
- [ ] 学習ログ分析が高速化（不要ファイルがない）
- [ ] ナレッジベースが他プロジェクトで実際に参照されている

---

## リスク評価

### 低リスク
- ファイルコピー（非破壊的）
- 新リポジトリ作成（既存に影響なし）
- ドキュメント更新

### 中リスク
- 1-2週間後のファイル削除（git reset可能だが手間）
- ファイルリネーム（検索性に影響）

### 高リスク
- 誤った `git rm` 実行による意図しない削除（大量削除時のヒューマンエラー）

**総合リスクレベル**：**中** - 段階的運用で軽減可能だが、クリーンアップ時は確認手順を厳格化する

---

## 重要ファイルパス

### 新プロジェクト作成で参照
- `/Users/310tea/Documents/学習アウトプット/README.md` - 命名規則参照
- `/Users/310tea/Documents/学習アウトプット/.gitignore` - テンプレート

### 更新が必要
- `/Users/310tea/Documents/学習アウトプット/README.md` - スコープ明確化
- `/Users/310tea/Documents/学習アウトプット/AGENTS.md` - ファイル配置ルール更新
- `/Users/310tea/Documents/学習アウトプット/CLAUDE.md` - 新プロジェクト参照追加

### 移行後の検証
- `/Users/310tea/Documents/学習アウトプット/.agent/skills/format_daily_log/` - 動作確認
- `/Users/310tea/Documents/学習アウトプット/.agent/skills/normalize_learning_log/` - 動作確認

---

## 検証手順

### 新プロジェクトコミット後
```bash
cd ~/Documents/学習ナレッジベース
find interviews -type f | wc -l  # 8ファイルを期待
find outputs -type f | wc -l     # 4ファイルを期待
git log --oneline  # Initial commitを確認
```

### 移行期間中（毎週）
```bash
cd ~/Documents/学習アウトプット
# format_daily_log スキル実行テスト
# normalize_learning_log スキル実行テスト
```

### クリーンアップ後
```bash
cd ~/Documents/学習アウトプット
ls docs/  # app_development_guide.mdが存在しないことを確認
test ! -d notes/app_ideas && echo "notes/app_ideas removed"
test ! -d outputs && echo "outputs removed"
test ! -d technical_interviews && echo "technical_interviews removed"
git status  # クリーンであることを確認
```
