# OBLスプリント資料集約プラン

## Context（なぜこの変更が必要か）

次回のOBLスプリント（2026-03-01 to 2026-04-11）を実行する際、スプリント中に参照すべき戦略文書・方法論・前回の実績データが複数のディレクトリに分散している。

**問題点：**
- outputs/, docs/, weekly_strategies/, Sessions/ など複数ディレクトリに資料が散在
- スプリント実行中に「どこに何があるか」を探す時間が発生
- 参照タイミング（Sprint前/Sprint中毎日/週次レビュー時）が明確でない
- 前回スプリントの教訓やパターンを見落とすリスク

**目的：**
次回OBLスプリント用のディレクトリ（`obl_sprint_project/2026-03-01_to_2026-04-11`）に、実行中に必要な資料を体系的に集約し、参照タイミング別に整理することで、スプリント実行効率を向上させる。

---

## 集約対象ファイル（探索結果より）

### 戦略・基盤ドキュメント（Critical）
1. `outputs/obl_sprint_retrospective_2026-01-12_to_2026-02-22.md` - 前回振り返り
2. `outputs/obl_strategy_report_2026-03-01.md` - 次サイクル戦略設計
3. `docs/obl_sprint_lessons_2026_q1.md` - 教訓リスト
4. `obl_sprint_project/OBL_sprint.md` - 基本フレームワーク
5. `obl_sprint_project/2026-03-01_to_2026-04-11/obl_schedule_report.md` - 詳細実行計画（既存）

### 方法論・パターン（High）
6. `docs/ai_learning_methodology.md` - 理論的基盤（哲学）
7. `docs/learning_success_patterns.md` - 成功パターン集
8. `docs/input_strategies/reading_methodology.md` - 読み方マニュアル
9. `docs/input_strategies/reading_trigger_design.md` - トリガー設計書

### 週次戦略（Critical）
10. `weekly_strategies/2026-03-01_to_2026-04-11_obl_cycle.json` - 週次計画

### 参考データ（前回スプリント）
11-15. `Sessions/Sessions_DB_2026-01-19_to_2026-02-22.md`（5週分）
16-18. `normalized_data/normalized_data_2026-01-20_to_2026-02-22.json`（3ファイル）

---

## ディレクトリ構造設計

```
obl_sprint_project/2026-03-01_to_2026-04-11/
├── README.md                          # ナビゲーションハブ（参照タイミング・優先度を記載）
├── obl_schedule_report.md            # 既存：詳細実行計画
│
├── 0_core/                           # Critical：Sprint前に必読
│   ├── OBL_sprint.md → ../../OBL_sprint.md
│   ├── obl_strategy_report_2026-03-01.md → ../../../outputs/obl_strategy_report_2026-03-01.md
│   └── obl_sprint_lessons_2026_q1.md → ../../../docs/obl_sprint_lessons_2026_q1.md
│
├── 1_foundations/                    # High：哲学・理論基盤（週次レビュー時）
│   ├── ai_learning_methodology.md → ../../../docs/ai_learning_methodology.md
│   └── learning_success_patterns.md → ../../../docs/learning_success_patterns.md
│
├── 2_playbooks/                      # High：実行マニュアル（日次・週次で頻繁に参照）
│   ├── reading_methodology.md → ../../../docs/input_strategies/reading_methodology.md
│   └── reading_trigger_design.md → ../../../docs/input_strategies/reading_trigger_design.md
│
├── 3_reference_data/                 # Medium：前回スプリントの参考データ
│   ├── retrospective/
│   │   └── obl_sprint_retrospective_2026-01-12_to_2026-02-22.md → ../../../../outputs/
│   └── sessions/
│       ├── Sessions_DB_2026-01-19_to_2026-01-25.md → ../../../../Sessions/
│       ├── Sessions_DB_2026-01-26_to_2026-02-01.md → ../../../../Sessions/
│       ├── Sessions_DB_2026-02-02_to_2026-02-08.md → ../../../../Sessions/
│       ├── Sessions_DB_2026-02-09_to_2026-02-15.md → ../../../../Sessions/
│       └── Sessions_DB_2026-02-16_to_2026-02-22.md → ../../../../Sessions/
│
├── 4_normalized_data/                # Low：分析データ（週次レビュー時の数値確認用）
│   ├── normalized_data_2026-01-20_to_2026-01-24.json → ../../../normalized_data/
│   ├── normalized_data_2026-01-26_to_2026-01-31.json → ../../../normalized_data/
│   └── normalized_data_2026-02-16_to_2026-02-22.json → ../../../normalized_data/
│
├── 5_weekly_strategy/                # Critical：週次計画（毎週日曜）
│   └── weekly_strategy_2026-03-01_to_2026-04-11_obl_cycle.json → ../../../weekly_strategies/
│
└── 6_logs/                           # スプリント終了後にコピー集約
    ├── daily/                        # 期間中のdaily logをコピー（終了後）
    ├── Sessions/                     # 期間中のSessions DBをコピー（終了後）
    ├── weekly_reviews/
    │   └── 2026/                     # 期間中の週次レビューをコピー（終了後、年フォルダ維持）
    └── sprint_final_review.md       # 新規作成：GO/PIVOT/KILL判定記録（終了後）
```

**命名規則の理由：**
- `0_core/`, `1_foundations/`等の番号プレフィックス：優先度順にソートされる
- 英語・小文字・アンダースコア区切り：CLAUDE.md命名規則に準拠

---

## ファイル配置方針

### 原則：シンボリックリンクを使用

**理由：**
1. 運用中のスプリントであり、元ファイルの更新を即座に反映する必要がある
2. learning_success_patterns.md等は週次で更新される可能性が高い
3. ディスク容量の節約、バージョン衝突の回避
4. CLAUDE.mdのset管理（6週間後のアーカイブ）とは異なる運用フェーズ

**例外：スプリント終了後（2026-04-12以降）**
- `6_logs/` 配下のdaily、Sessions、weekly_reviewsは**コピー**で集約
- 理由：アーカイブとして固定し、元ファイルとは独立管理

### Sessions拡張子の運用方針（このスプリント）
- 本スプリントでは `Sessions_DB_*.md` を運用ログとして使用する
- AGENTS.mdの `Sessions_DB_*.csv` はNotionエクスポート由来の正規命名として維持し、必要に応じて並行管理する

---

## 実装手順

### Phase 1: 初期構築（スプリント開始前）

```bash
# ベースディレクトリ設定
BASE_DIR="/Users/310tea/Documents/Learning_log/obl_sprint_project/2026-03-01_to_2026-04-11"
cd "$BASE_DIR"

# 1. サブディレクトリ作成
mkdir -p 0_core 1_foundations 2_playbooks \
         3_reference_data/retrospective 3_reference_data/sessions \
         4_normalized_data 5_weekly_strategy \
         6_logs/daily 6_logs/Sessions 6_logs/weekly_reviews/2026

# 2. 0_core/ のシンボリックリンク作成
cd "$BASE_DIR/0_core"
ln -sfn ../../OBL_sprint.md OBL_sprint.md
ln -sfn ../../../outputs/obl_strategy_report_2026-03-01.md obl_strategy_report_2026-03-01.md
ln -sfn ../../../docs/obl_sprint_lessons_2026_q1.md obl_sprint_lessons_2026_q1.md

# 3. 1_foundations/ のシンボリックリンク作成
cd "$BASE_DIR/1_foundations"
ln -sfn ../../../docs/ai_learning_methodology.md ai_learning_methodology.md
ln -sfn ../../../docs/learning_success_patterns.md learning_success_patterns.md

# 4. 2_playbooks/ のシンボリックリンク作成
cd "$BASE_DIR/2_playbooks"
ln -sfn ../../../docs/input_strategies/reading_methodology.md reading_methodology.md
ln -sfn ../../../docs/input_strategies/reading_trigger_design.md reading_trigger_design.md

# 5. 3_reference_data/ のシンボリックリンク作成
cd "$BASE_DIR/3_reference_data/retrospective"
ln -sfn ../../../../outputs/obl_sprint_retrospective_2026-01-12_to_2026-02-22.md obl_sprint_retrospective_2026-01-12_to_2026-02-22.md

cd "$BASE_DIR/3_reference_data/sessions"
ln -sfn ../../../../Sessions/Sessions_DB_2026-01-19_to_2026-01-25.md Sessions_DB_2026-01-19_to_2026-01-25.md
ln -sfn ../../../../Sessions/Sessions_DB_2026-01-26_to_2026-02-01.md Sessions_DB_2026-01-26_to_2026-02-01.md
ln -sfn ../../../../Sessions/Sessions_DB_2026-02-02_to_2026-02-08.md Sessions_DB_2026-02-02_to_2026-02-08.md
ln -sfn ../../../../Sessions/Sessions_DB_2026-02-09_to_2026-02-15.md Sessions_DB_2026-02-09_to_2026-02-15.md
ln -sfn ../../../../Sessions/Sessions_DB_2026-02-16_to_2026-02-22.md Sessions_DB_2026-02-16_to_2026-02-22.md

# 6. 4_normalized_data/ のシンボリックリンク作成
cd "$BASE_DIR/4_normalized_data"
ln -sfn ../../../normalized_data/normalized_data_2026-01-20_to_2026-01-24.json normalized_data_2026-01-20_to_2026-01-24.json
ln -sfn ../../../normalized_data/normalized_data_2026-01-26_to_2026-01-31.json normalized_data_2026-01-26_to_2026-01-31.json
ln -sfn ../../../normalized_data/normalized_data_2026-02-16_to_2026-02-22.json normalized_data_2026-02-16_to_2026-02-22.json

# 7. 5_weekly_strategy/ のシンボリックリンク作成
cd "$BASE_DIR/5_weekly_strategy"
ln -sfn ../../../weekly_strategies/2026-03-01_to_2026-04-11_obl_cycle.json weekly_strategy_2026-03-01_to_2026-04-11_obl_cycle.json

# 8. 検証
cd "$BASE_DIR"
find . -type l -ls  # すべてのシンボリックリンクを表示
```

### Phase 2: README.md作成

README.mdに以下の内容を記載：
- このディレクトリの使い方（参照タイミング別ガイド）
- スプリント開始前に読むべきファイル（0_core/の3ファイル + obl_schedule_report.md）
- スプリント実行中に参照するファイル（2_playbooks/を毎日、1_foundations/を週次）
- ディレクトリ構造の設計原則（優先度・参照タイミング）
- GO/PIVOT/KILL判定基準
- シンボリックリンクの管理方法

### Phase 3: スプリント終了後（2026-04-12以降）

```bash
# 期間中のログファイルをコピー集約
BASE_DIR="/Users/310tea/Documents/Learning_log/obl_sprint_project/2026-03-01_to_2026-04-11"
ROOT_DIR="/Users/310tea/Documents/Learning_log"
SPRINT_START="2026-03-01"
SPRINT_END="2026-04-11"

# daily/ のコピー（期間内ファイルのみ）
for f in "$ROOT_DIR"/daily/daily_*.md; do
  [ -e "$f" ] || continue
  d="${f##*/daily_}"
  d="${d%.md}"
  if [[ "$d" >= "$SPRINT_START" && "$d" <= "$SPRINT_END" ]]; then
    cp "$f" "$BASE_DIR/6_logs/daily/"
  fi
done

# Sessions/ のコピー（開始日・終了日がともに期間内の .md のみ）
for f in "$ROOT_DIR"/Sessions/Sessions_DB_*.md; do
  [ -e "$f" ] || continue
  n="${f##*/}"
  if [[ "$n" =~ ^Sessions_DB_([0-9]{4}-[0-9]{2}-[0-9]{2})_to_([0-9]{4}-[0-9]{2}-[0-9]{2})\.md$ ]]; then
    s="${BASH_REMATCH[1]}"
    e="${BASH_REMATCH[2]}"
    if [[ "$s" >= "$SPRINT_START" && "$e" <= "$SPRINT_END" ]]; then
      cp "$f" "$BASE_DIR/6_logs/Sessions/"
    fi
  fi
done

# weekly_reviews/ のコピー（開始日・終了日がともに期間内、年フォルダ維持）
for f in "$ROOT_DIR"/weekly_reviews/2026/weekly_*.md; do
  [ -e "$f" ] || continue
  n="${f##*/}"
  if [[ "$n" =~ ^weekly_([0-9]{4}-[0-9]{2}-[0-9]{2})_to_([0-9]{4}-[0-9]{2}-[0-9]{2})\.md$ ]]; then
    s="${BASH_REMATCH[1]}"
    e="${BASH_REMATCH[2]}"
    if [[ "$s" >= "$SPRINT_START" && "$e" <= "$SPRINT_END" ]]; then
      cp "$f" "$BASE_DIR/6_logs/weekly_reviews/2026/"
    fi
  fi
done

# sprint_final_review.md を手動作成（GO/PIVOT/KILL判定記録）
```

---

## Critical Files（実装で最も重要なファイル）

1. **README.md**（新規作成）- ナビゲーションハブとして全体ガイドを提供
2. **0_core/** - 3つの戦略文書をシンボリックリンクで集約
3. **2_playbooks/** - 日次参照用の実行マニュアルを集約
4. **5_weekly_strategy/** - 週次計画JSONをシンボリックリンクで配置

**オプション：**
- `2_playbooks/tech_interview_prep_template.md` - 技術面談3段階プロセステンプレート（新規作成）
  - obl_strategy_report_2026-03-01.mdに定義されている内容を抽出して独立テンプレート化
  - 実装時に必要性を判断

---

## 検証方法

```bash
# シンボリックリンクが正しく機能するかテスト
cd /Users/310tea/Documents/Learning_log/obl_sprint_project/2026-03-01_to_2026-04-11
cat 0_core/OBL_sprint.md | head -5  # リンク先ファイルの内容が表示されるはず

# ディレクトリ構造確認
ls -R

# シンボリックリンク一覧確認
find . -type l -ls
```

---

## CLAUDE.md整合性確認

### ディレクトリ配置ルール
- ✅ `obl_sprint_project/` は既存ディレクトリ、README.mdのSection 4に記載あり
- ✅ 運用中のスプリントはシンボリックリンク、終了後はCOPY（set管理と同様の原則）

### 命名規則
- ✅ 英語・小文字・アンダースコア区切り（`0_core`, `reading_methodology.md`）
- ✅ 日付形式はYYYY-MM-DD（ISO 8601）
- ✅ バージョン番号なし（git管理）

### ファイル操作
- ✅ 既存ファイルはRead後にシンボリックリンク作成（`ln -sfn`で再実行可能）
- ✅ 新規ファイルはREADME.md、sprint_final_review.md（終了後）のみ
