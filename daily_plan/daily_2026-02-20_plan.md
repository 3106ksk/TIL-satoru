# 2026-02-20（金）Shift Day — 学習計画

## ■ Context

- **Day Mode**: Shift
- **Budget**: 90 min（18:00以降の帰宅後学習）
- **前日**: 2/19 Focus Day → 513 min学習（Budget 360 minの142.5%）、DS 3.72
- **2/19の成果**:
  - ✅ rails new + GitHub push 完了（18:02）
  - ✅ Devise・tag・UX検索の技術選定完了（bcrypt、ransack + LLM方針確定）
  - ✅ テーブル設計・ER図作成完了
  - ✅ 技術選定リスト（Markdown）の成果物化完了
- **認知リソース状況**: 前日513 minの学習でバーンアウト兆候（Headroom=2で夜間まとめ作業失敗）→ 回復不十分の可能性

---

## ■ Top1 / Done条件

**Top1**: ルーティング設計（routes.rb）の基本構成完成

**Done条件**: 19:30までに、CRUD基本構造のroutes.rbが設計され、GitHubにpushされている状態

**内容**:
- 学習Tips掲示板アプリのリソース設計（articles, categories, users, tags）
- RESTfulなルーティング構成のスケッチ
- ネストしたルーティングの必要性判断（例: articles/categories）

**切れたら→**: なし（90分で確実に終了。次のタスクは明日）

---

## ■ 本日のタスクシーケンス

### 🌙 夜間ブロック（Shift帰宅後 18:00-19:30）

| ステップ | タスク | 目安時間 | メモ |
|---|---|---|---|
| 1 | この計画を読む | 5 min | Top1 + Done条件のみ確認 |
| 2 | カリキュラムのroutes復習 | 15-20 min | resourcesの基本、nested routesの復習。新規学習は不要 |
| 3 | ER図からリソース抽出 | 10 min | 2/19作成のER図を見ながら必要なリソースを列挙 |
| 4 | routes.rb設計 | 30-40 min | RESTfulな構成でスケッチ。深追い禁止 |
| 5 | GitHub push | 5-10 min | コミットメッセージ: "feat: add basic routing structure" |

> ⏱️ **90分タイムボックス**: Shift帰宅後の疲労 + 前日のバーンアウト兆候を考慮し、90分で確実に終了する。Controller実装・View作成は一切行わず、ルーティング設計のみに集中。

---

## ■ リスク対策（If-Then）

| リスク | If（トリガー） | Then（対処） |
|---|---|---|
| Shift疲労で帰宅後に集中できない | 帰宅時にHeadroom≦2を感じる | カリキュラム復習を飛ばし、最小限のroutes.rb（articlesのCRUDのみ）で完了 |
| ネストルーティングで固着 | 30min超えて進展なし | ネストなしのフラットな構成で確定。複雑な設計は日曜に見直し |
| 90分で終わらない | 19:00時点で未完成 | articlesとusersの2リソースのみ確定してpush。残りは明日 |
| 疲労で学習自体を開始できない | 18:30を過ぎても着手できていない | 完全休養日に切り替え。無理な学習はバーンアウトリスクを高めるだけ |

---

## ■ 週次ゴールとの接続

```
週次成功条件: ミニアプリの基本構造（rails new → DB設計 → 主要画面のCRUD）が動作
残りスケジュール: 今日(金)Shift → 土Shift → 日曜Off
```

**今日の90分を達成すれば**:
- ルーティング構成が確定 → 明日(土)のController雛形作成がスムーズに進む
- 土曜も90分程度の低負荷タスク（Controller雛形のみ）で繋ぎ、日曜にCRUD実装へ集中できる
- 週次ゴールの「主要画面のCRUD」への射程圏内を維持

**今日やらなくてよいこと**:
- Controllerの実装
- Viewファイルの作成
- ルーティングの完璧な最適化（後から修正可能）

---

## ■ Stats（夜間学習後に記入）

- **Total Min**: —
- **純粋な学習時間**: —
- **Avg Deep Score**: —
- **Top1 達成**: —

## ■ Worked / Slipped / Insights（夜に記入）

---

## ■ Study Strategy for Next Day

> （夜の振り返り時に記入）
