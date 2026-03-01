# OBL Sprint 2026-03-01 to 2026-04-11 - Navigation Hub

## Sprint Overview

次回OBLスプリント（2026-03-01 to 2026-04-11, 6週間）の実行に必要な戦略文書・方法論・参考データを体系的に集約したディレクトリです。

**目的**: スプリント実行中に「どこに何があるか」を探す時間を削減し、参照タイミング別に整理された資料を効率的にアクセスできるようにする。

---

## Quick Start Guide

### スプリント開始前に必読（Critical）

以下の4ファイルをスプリント開始前に必ず読んでおくこと:

1. [OBL_sprint.md](0_core/OBL_sprint.md) - OBLスプリントの基本フレームワーク
2. [obl_strategy_report_2026-03-01.md](0_core/obl_strategy_report_2026-03-01.md) - 次サイクル戦略設計
3. [obl_sprint_lessons_2026_q1.md](0_core/obl_sprint_lessons_2026_q1.md) - 前回スプリントの教訓リスト
4. [obl_schedule_report.md](obl_schedule_report.md) - 詳細実行計画（既存ファイル）

---

## Directory Structure & Usage

### 0_core/ - Critical: Sprint前に必読

**参照タイミング**: スプリント開始前 + 週次レビュー時

戦略の核となる3つのドキュメント:
- `OBL_sprint.md` - OBLスプリントの基本フレームワーク（GO/PIVOT/KILL判定基準）
- `obl_strategy_report_2026-03-01.md` - 次サイクル戦略設計（技術面談3段階プロセス含む）
- `obl_sprint_lessons_2026_q1.md` - 前回スプリントで得られた教訓（失敗パターン・成功要因）

### 1_foundations/ - High: 哲学・理論基盤

**参照タイミング**: 週次レビュー時、方向性に迷った時

学習方法論の理論的基盤:
- `ai_learning_methodology.md` - AI活用学習の哲学（Input/Process/Outputサイクル、メタ認知）
- `learning_success_patterns.md` - 実証済みの成功パターン集

### 2_playbooks/ - High: 実行マニュアル

**参照タイミング**: 日次・週次で頻繁に参照

日々の実践で使う実行マニュアル:
- `reading_methodology.md` - 技術記事の読み方マニュアル（3段階プロセス）
- `reading_trigger_design.md` - 読解トリガーの設計書（質問テンプレート）

### 3_reference_data/ - Medium: 前回スプリントの参考データ

**参照タイミング**: 週次レビュー時の比較分析、パターン確認

前回スプリント（2026-01-12 to 2026-02-22）の実績データ:
- `retrospective/` - 振り返りレポート
- `sessions/` - 週次Sessionsログ（5週分）

### 4_normalized_data/ - Low: 分析データ

**参照タイミング**: 週次レビュー時の数値確認

前回スプリントの正規化データ（JSON形式、3ファイル）

### 5_weekly_strategy/ - Critical: 週次計画

**参照タイミング**: 毎週日曜の週次計画策定時

6週間分の週次戦略を記載したJSONファイル:
- `weekly_strategy_2026-03-01_to_2026-04-11_obl_cycle.json`

### 6_logs/ - スプリント終了後に集約

**参照タイミング**: スプリント終了後（2026-04-12以降）

スプリント期間中に生成されたログをコピー集約する場所:
- `daily/` - 期間中のdaily logをコピー
- `Sessions/` - 期間中のSessions DBをコピー
- `weekly_reviews/2026/` - 期間中の週次レビューをコピー
- `sprint_final_review.md` - GO/PIVOT/KILL判定記録（新規作成）

---

## Daily & Weekly Workflow

### 日次（毎日）

1. **朝**: [obl_schedule_report.md](obl_schedule_report.md) で今日のタスク確認
2. **学習中**: [2_playbooks/reading_methodology.md](2_playbooks/reading_methodology.md) を参照しながら実行
3. **夜**: Daily Reviewを作成し、`6_logs/daily/` に保存（スプリント終了後にコピー集約）

### 週次（毎週日曜）

1. **週次戦略確認**: [5_weekly_strategy/weekly_strategy_2026-03-01_to_2026-04-11_obl_cycle.json](5_weekly_strategy/weekly_strategy_2026-03-01_to_2026-04-11_obl_cycle.json) で今週の計画を確認
2. **振り返り**: [1_foundations/learning_success_patterns.md](1_foundations/learning_success_patterns.md) と照合して今週の成果を評価
3. **教訓確認**: [0_core/obl_sprint_lessons_2026_q1.md](0_core/obl_sprint_lessons_2026_q1.md) で失敗パターンを回避できているか確認
4. **週次レビュー作成**: `6_logs/weekly_reviews/2026/` に保存（スプリント終了後にコピー集約）

---

## GO/PIVOT/KILL Judgment Criteria

スプリント終了時（2026-04-12）に以下の基準で判定する:

### GO（継続）
- 技術面談で明確な手応えがある（3段階プロセスが機能している）
- Deep Scoreが週次で向上傾向にある
- Learning Success Patternsに合致した学習ができている

### PIVOT（方向転換）
- 技術面談の準備時間が学習時間を圧迫している
- Deep Scoreが停滞または低下している
- 「わかったつもり」が増えている（Cognitive Headroom減少）

### KILL（中止）
- 6週間で明確な改善が見られない
- 方法論と実践が乖離している
- 技術面談の価値を実感できない

判定結果は `6_logs/sprint_final_review.md` に記録すること。

---

## File Management Notes

### シンボリックリンクについて

このディレクトリ内のほとんどのファイルはシンボリックリンクです。元ファイルの更新が即座に反映されるため、常に最新の内容を参照できます。

**検証コマンド**:
```bash
# シンボリックリンク一覧確認
find . -type l -ls

# リンク先ファイルの内容確認
cat 0_core/OBL_sprint.md | head -5
```

### スプリント終了後の作業（2026-04-12以降）

期間中のログファイルを `6_logs/` 配下にコピー集約する:
- `daily/` - daily_2026-03-01.md ~ daily_2026-04-11.md
- `Sessions/` - Sessions_DB_*.md（開始日・終了日がともに期間内）
- `weekly_reviews/2026/` - weekly_*.md（開始日・終了日がともに期間内）

**重要**: スプリント終了後はCOPYでアーカイブ化し、元ファイルとは独立管理する。

---

## Related Documents

- [../../CLAUDE.md](../../CLAUDE.md) - プロジェクト全体のルール
- [../../AGENTS.md](../../AGENTS.md) - ファイル配置・命名規則
- [../../obl_sprint_project/OBL_sprint.md](../OBL_sprint.md) - OBLスプリント基本フレームワーク

---

**Last Updated**: 2026-02-23
