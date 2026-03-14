# 学習Tipsお悩み相談所 投稿機能フォーム実装リサーチ

作成日: 2026-03-06
参照元: `learning_tips_consultation.md`

## 前提技術スタック

この設計書で前提になっている投稿機能の実装環境は以下。

| 項目 | 前提 |
| --- | --- |
| バックエンド | Ruby on Rails |
| UI基盤 | ERB |
| フロント補助 | Hotwire |
| JavaScript | Stimulus |
| CSS | Tailwind CSS |
| UIコンポーネント | daisyUI |
| DB | PostgreSQL |
| 認証 | `has_secure_password` 相当の `bcrypt` + セッション認証 |
| 画像アップロード | CarrierWave |
| 画像処理 | MiniMagick |
| ページネーション | Kaminari |
| デプロイ想定 | Render |

## 結論

投稿フォーム実装で理解が必須なのは、`Rails form_with`、Strong Parameters、モデルバリデーション、ERBでのフォーム描画、カテゴリ/タグの選択UI、Stimulusによる補助UI、関連テーブルを含む保存処理。

特にこのアプリでは、自由記述フォームではなく、**構造化された投稿フォーム**として以下を正しく扱う必要がある。

- 必須項目: `title`, `problem`, `hypothesis`, `action`, `learning`, `category_id`
- 任意項目: `reference`
- 複数選択: `tag_ids`

## フォーム実装で必須理解の要件・技術一覧

| 区分 | 要件/技術 | 必須度 | このアプリで必要な理由 | 実装時の着眼点 |
| --- | --- | --- | --- | --- |
| フォーム基盤 | `form_with` | 必須 | Tips投稿ページ `/tips/new` の入力UIを作る中心になるため | `model: @tip` を使い、create失敗時も入力値を保持する |
| パラメータ制御 | Strong Parameters | 必須 | 投稿データとタグ配列を安全に保存するため | `tag_ids: []` を許可する必要がある |
| モデル設計 | Active Record / Association | 必須 | `Tip belongs_to :user, :category`、`Tip has_many :tags, through: :tip_tags` が前提のため | 中間テーブル経由の保存・取得を理解する |
| バリデーション | `presence`, `length`, URL妥当性 | 必須 | 設計書上、各項目の必須/文字数制約が明確なため | `title` 100字、本文系は推奨100-200字をどう扱うかを決める |
| ビュー | ERB | 必須 | Rails + ERB前提でフォーム画面を構築するため | フォーム部品とエラーメッセージ表示を部分テンプレート化しやすい |
| CSS | Tailwind CSS | 必須 | 入力欄、レイアウト、視覚フィードバックを整えるため | エラー状態、必須表示、入力支援UIの見た目を揃える |
| UI部品 | daisyUI | 必須寄り | 設計書で採用決定になっており、フォームの見た目を高速実装できるため | `input`, `textarea`, `select`, `radio`, `checkbox`, `button` を活用 |
| JS補助 | Stimulus | 必須寄り | 文字数カウンター、ヘルプ表示、モーダルなどの補助UIに必要 | フォームでは特に文字数カウンター実装で重要 |
| 非同期遷移基盤 | Turbo / Hotwire | 理解推奨 | Rails + Hotwire前提のため、フォーム送信時の挙動理解が必要 | 初期実装は通常POSTでもよいが、Turboとの競合は把握する |
| 認証 | `bcrypt` + セッション認証 | 必須 | ログインユーザーのみ投稿可能という要件のため | `current_user.tips.build` の形で投稿者を紐づける |
| データ設計 | `categories` テーブル | 必須 | カテゴリ選択が投稿フォーム要件に含まれるため | ラジオかセレクトかをUI方針に合わせる |
| データ設計 | `tags`, `tip_tags` | 必須 | 投稿時のタグ選択式付与がMVP要件のため | チェックボックス複数選択で実装する |
| ファイル設計 | CarrierWave | 不要 | 投稿フォーム本体には不要。ユーザーアイコン表示側で使う | 投稿フォームではなくプロフィール編集で主に使う |
| 一覧連携 | Kaminari | 不要 | 投稿フォーム自体には不要だが、投稿完了後の一覧画面で使う | 作成後リダイレクト先の表示件数に影響する |

## フォーム項目別に理解が必要なこと

| フォーム項目 | 型/入力UI | 保存先 | 理解必須のポイント |
| --- | --- | --- | --- |
| タイトル | `text_field` | `tips.title` | 100文字以内の制約、一覧で流し読みされる前提 |
| 課題 | `text_area` | `tips.problem` | 問題提起の主軸。必須項目 |
| 仮説・思考 | `text_area` | `tips.hypothesis` | この設計で最重要カラム。必須項目 |
| 具体的な行動 | `text_area` | `tips.action` | 再現可能なアクションを書く欄。必須項目 |
| 学び | `text_area` | `tips.learning` | 結果と気づきの統合欄。必須項目 |
| 参考URL | `url_field` または `text_field` | `tips.reference` | 任意入力。URL形式のバリデーション判断が必要 |
| カテゴリ | `radio_button` または `select` | `tips.category_id` | MVPではカテゴリタブと連動する重要軸 |
| タグ | `check_box` 複数 | `tip_tags` 経由 | 開発者定義済みタグの選択式。自由入力ではない |

## 投稿フォームで調べるべきライブラリ/技術の優先順位

| 優先度 | 技術/ライブラリ | 調べるべき内容 | 調査理由 |
| --- | --- | --- | --- |
| 高 | Rails `form_with` | モデル連携フォーム、エラー再表示、`collection_check_boxes` | 実装の中心になるため |
| 高 | Strong Parameters | 配列パラメータ、ネストなしの安全な受け取り | タグ複数選択保存で必須 |
| 高 | Active Record Association | `has_many :through` の保存と表示 | `tips` と `tags` の関係実装に必要 |
| 高 | Active Model Validation | `presence`, `length`, 独自URLバリデーション | フォーム品質の担保に必要 |
| 高 | Stimulus | 文字数カウンター、ヘルプ表示切替 | 設計書の入力支援UIに直結 |
| 高 | daisyUI | Railsフォーム部品へのクラス適用 | MVPの高速UI実装に直結 |
| 中 | Turbo | フォーム送信後の遷移、エラー表示時の挙動 | Hotwire前提のため事故防止に必要 |
| 中 | Tailwind CSS | フォームレイアウト、状態別スタイル | UI品質の土台になるため |
| 中 | Rails Routing / REST | `new`, `create`, `show`, `index` の流れ | 投稿機能全体の接続理解に必要 |
| 低 | CarrierWave | アバター表示との連携確認 | 投稿フォーム直接要件ではないため |
| 低 | Kaminari | 作成後の一覧表示 | 投稿画面そのものではないため |
| 低 | Ransack | 将来のタグ絞り込み | v1.5以降のため現時点では必須でない |
| 低 | pg_search | 自由記述検索 | v2.0以降のため現時点では不要 |

## v1.0のフォーム実装で最低限必要な画面仕様

| 項目 | 内容 |
| --- | --- |
| 画面URL | `/tips/new` |
| 送信先 | `POST /tips` |
| 送信成功時 | Tips一覧ページへリダイレクト |
| 送信失敗時 | 投稿フォーム再表示 + エラー表示 + 入力値保持 |
| 入力支援 | プレースホルダー、文字数カウンター、書き方のコツ表示 |
| 必須UI | タイトル、課題、仮説・思考、具体的な行動、学び、参考URL、カテゴリ選択、タグ選択 |

## 実装前に明確化しておくべき仕様

| 論点 | 決めるべきこと |
| --- | --- |
| 文字数制約 | 100-200文字を「必須制約」にするか「推奨表示」にするか |
| 参考URL | URL形式バリデーションを厳密に入れるか |
| カテゴリUI | ラジオボタンにするかセレクトボックスにするか |
| タグUI | カテゴリ別グルーピング表示をするか |
| 入力支援 | 文字数カウンターをStimulusでリアルタイム更新するか |
| エラー表示 | 項目上部集約か、各入力欄の直下表示か |

## いまの設計書を前提にした実装優先順位

1. `Tip`, `Category`, `Tag`, `TipTag` のモデルと関連を確定
2. `tips#new`, `tips#create` と Strong Parameters を実装
3. ERB + daisyUI で構造化フォームを作成
4. バリデーションとエラー表示を実装
5. Stimulusで文字数カウンターを追加
6. 投稿完了後の一覧リダイレクトと表示確認
7. 必要に応じてTurboとの挙動を調整
