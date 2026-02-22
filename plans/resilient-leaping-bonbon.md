# 学習Tipsお悩み相談所 - 技術調査項目の整理

## Context

`notes/app_ideas/learning_tips_consultation.md` のミニアプリ開発において、①〜④のセクションで要件定義、UX設計、MVP範囲、リスク管理が完了している。⑤の「技術選定と調査」セクションが空のままなので、前セクションの内容から必要な技術調査項目を抽出・整理する必要がある。

**前提条件:**
- ミニアプリレベル（Rails標準技術スタック中心、コア機能のみでリリース優先）
- RUNTEQ生限定アクセスなし（シンプルな認証のみ）
- 外部サービス連携なし（Discord API、note記事インポートは対象外）
- 画像はテキストベースのみ、ただしユーザーアイコンは gem carrierwave で管理
- 下書き保存機能なし（技術量削減）
- UI設計：タブ切り替え＋シンプルなリスト表示（カード型レイアウトではない）
- Rails + PostgreSQL + Hotwire を前提とした調査項目

この作業により、実装前に調査すべき技術要素が明確になり、ミニアプリとして最小限の技術スタックでリリース可能な計画が立てられる。

## Implementation Plan

### 追加する内容の構成

⑤セクションに以下のカテゴリで技術調査項目を追加する：

#### 1. フロントエンド技術スタック
**調査項目：**
- タブ切り替え＋シンプルなリスト表示の実装
  - Rails標準のerb + TailwindCSS
  - タブUI（シンプルなCSSクラス切り替え）
- モーダル表示の実装パターン（投稿者プロフィール詳細表示用）
- フィルタリング機能（カテゴリ、新着順/評価順の切り替え）

#### 2. バックエンド・ルーティング設計
**調査項目：**
- Railsの標準的なRESTful設計（resources routing）
- Tips投稿のバリデーション（モデルレベル、presence/lengthなど）
- フィルタリング・ソート処理（scopeの活用、シンプルなwhere/order）
- ページネーション（kaminari or pagy gem）

#### 3. データベース設計
**調査項目：**
- テーブル設計
  - Users（プロフィール、タグ情報、アイコン保存パス）
  - Tips（構造化フィールド：situation/tried/result/learning + カテゴリ外部キー）
  - Categories（カテゴリマスタ）
  - Reactions（「参考になった」カウント、中間テーブルか単純カウンタか）
- インデックス設計（category_id, created_at, user_idなど）
- PostgreSQL（RUNTEQ推奨）を前提としたマイグレーション設計
- アソシエーション設計（has_many, belongs_to, through）

#### 4. 認証・ユーザー管理
**調査項目：**
- gem deviseでの基本認証実装（email/password）
- ユーザープロフィール管理
  - 本業有無、学習期間、現在のフェーズなどのタグ情報
  - carrierwaveでのアイコン画像アップロード・表示
- carrierwaveの基本設定（ローカルストレージ、画像リサイズはMiniMagick）

#### 5. AI機能統合（v2.0以降、参考程度）
**調査項目：**
- OpenAI API or Anthropic Claude APIの基本的な使い方
- Tips推薦のための簡単なプロンプト設計
- コスト試算（少数ユーザー想定）

#### 6. デプロイ・インフラ
**調査項目：**
- ホスティングサービスの選定
  - Heroku（RUNTEQ推奨、シンプルなデプロイ）
  - Render, Railway（無料枠の制限確認）
- 環境変数管理（credentials.yml.enc or dotenv gem）
- PostgreSQLのホスティング（Heroku Postgres or 外部サービス）

#### 7. 初期データ・運用準備
**調査項目：**
- シード投稿の準備方法（seeds.rbでの初期データ投入）
- 初期データ不足時のUI設計（空状態の表示）
- 投稿完了率の簡易トラッキング（Railsのログ分析 or シンプルなカウンター）

### 技術選定の優先順位（ミニアプリ・コア機能のみ）

**MVP v1.0で必須の調査項目（高優先度）:**
1. Rails標準でのフロントエンド実装（erb + TailwindCSS、タブはCSSクラス切り替え）
2. データベース設計（PostgreSQL前提、シンプルなテーブル構成）
3. gem devise（認証）
4. gem carrierwave（アイコン管理）
5. シンプルなフィルタリング（scopeでの実装）
6. ページネーション（kaminari or pagy gem）
7. デプロイ先の選定（Heroku優先）

**v1.5以降で検討（中優先度）:**
8. 全文検索機能（pg_search gem）
9. 投稿完了率の可視化

**v2.0以降で検討（低優先度）:**
10. AI機能統合（OpenAI/Claude API）

## Critical Files
- `/Users/310tea/Documents/学習アウトプット/notes/app_ideas/learning_tips_consultation.md` - 編集対象ファイル

## Verification

1. ⑤セクションに上記の調査項目が構造的に記載されていることを確認
2. ①〜④の要件（フォーム構造、フィルタリング、AI提案など）が漏れなく技術調査項目に反映されているか確認
3. MVP v1.0の範囲と後回し機能が明確に区別されているか確認
4. ファイルの可読性（見出しレベル、リスト構造）が保たれているか確認
