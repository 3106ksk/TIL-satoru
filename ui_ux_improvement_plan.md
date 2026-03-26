# UI/UX 改善計画書

## 1. 修正が必要なページ一覧

### 共通レイアウト

| ファイル | 問題点 | 改善内容 |
|---|---|---|
| `app/views/layouts/application.html.erb` | flashメッセージの表示コードが存在しない / `<main>`にpadding等なし | flashメッセージ表示ブロックを追加 / レイアウトの余白を整える |
| `app/views/shared/_header.html.erb` | 素の`<ul>`タグのみ、スタイル皆無 | daisyUI `navbar` コンポーネントに刷新 |
| `app/views/shared/_before_login_header.html.erb` | 素の`<ul>`タグのみ | daisyUI `navbar` コンポーネントに刷新 |

---

### 認証系ページ

| ファイル | 対応URL | 問題点 | 改善内容 |
|---|---|---|---|
| `app/views/users/new.html.erb` | `/signup` | 素のフォーム、ラベルも英語のまま、タイトルなし | daisyUI `card` + `input` / ラベル日本語化 / ページタイトル追加 / ログインへの導線リンク追加 |
| `app/views/user_sessions/new.html.erb` | `/login` | 素のフォーム、ボタン名が「ログインボタン」 | daisyUI `card` + `input` / ボタン名修正 / 新規登録への導線リンク追加 |

---

### Tips系ページ

| ファイル | 対応URL | 問題点 | 改善内容 |
|---|---|---|---|
| `app/views/tips/index.html.erb` | `/tips` | カテゴリフィルターがスタイル不足 / 選択中カテゴリのアクティブ状態がない | daisyUI `tab` コンポーネントに変更 / アクティブタブのハイライト実装 |
| `app/views/tips/_tip.html.erb` | `/tips`（部分テンプレート） | カード幅が固定`w-96` / 課題と行動のみ表示でタイトルの視認性が低い / 投稿者情報なし | レスポンシブ対応 / タイトルを主役に / 投稿者名・カテゴリバッジを追加 |
| `app/views/tips/new.html.erb` | `/tips/new` | 完全に素のフォーム / ラベルが英語 / プレースホルダーなし / 文字数カウンターなし | daisyUI `form` スタイル適用 / ラベル日本語化 / 設計書記載のプレースホルダーを追加 / 各セクションに説明文を追加 |
| `app/views/tips/show.html.erb` | `/tips/:id` | 著者名が「Sarah_Dev」とハードコード / アバターが外部URL直書き / 「一覧に戻る」リンクがスタイルなし | `@tip.user.name` に差し替え / アバター表示をプレースホルダーに変更 / リンクをボタン化 |

---

### プロフィール系ページ

| ファイル | 対応URL | 問題点 | 改善内容 |
|---|---|---|---|
| `app/views/profiles/show.html.erb` | `/profile` | Bootstrapクラス混在（`col-md-10`等）でスタイル未適用 / 「プロフィール画像」が固定テキスト | Tailwind / daisyUI に全面置換 / アバタープレースホルダーを表示 |
| `app/views/profiles/edit.html.erb` | `/profile/edit` | Bootstrapクラス混在（`form-control`, `btn btn-primary`等）でスタイル未適用 / introductionフィールドなし | Tailwind / daisyUI に全面置換 / introductionフィールドを追加 |

---

### ランディングページ

| ファイル | 対応URL | 問題点 | 改善内容 |
|---|---|---|---|
| `app/views/static_pages/top.html.erb` | `/` | プレースホルダーテキストのみ、実質未実装 | ヒーローセクション / アプリのコンセプト説明 / CTAボタン（新規登録・ログイン）を実装 |

---

## 2. フラッシュメッセージ改善一覧

### 問題の全体像

現状、コントローラーでflashを設定しているがレイアウトに表示コードが存在しないため、**ユーザーには一切表示されていない。**
また、i18nキーの参照先（`ja.yml`）が存在せず、翻訳が取得できていない。

---

### コントローラーごとのflash設定状況

| コントローラー | アクション | flash種別 | i18nキー / メッセージ | 状態 |
|---|---|---|---|---|
| `ApplicationController` | `require_login`（before_action） | `danger` | `defaults.flash_message.require_login` | キー未定義 |
| `UsersController` | `create` 成功時 | `notice` | `"ユーザーが作成されました。"` | ハードコード（i18n未使用） |
| `UsersController` | `create` 失敗時 | なし | — | 未実装 |
| `UserSessionsController` | `create` 成功時 | `success` | `user_sessions.create.success` | キー未定義 |
| `UserSessionsController` | `create` 失敗時 | なし | — | 未実装 |
| `UserSessionsController` | `destroy` 成功時 | `success` | `user_sessions.destroy.success` | キー未定義 |
| `TipsController` | `create` 成功時 | `success` | `tips.create.success` | キー未定義 |
| `TipsController` | `create` 失敗時 | なし | — | 未実装 |
| `ProfilesController` | `update` 成功時 | なし | — | 未実装 |
| `ProfilesController` | `update` 失敗時 | なし | — | 未実装 |

---

### 対応が必要な作業

| 作業 | ファイル | 内容 |
|---|---|---|
| レイアウトへの表示追加 | `app/views/layouts/application.html.erb` | `flash`をdaisyUI `alert`コンポーネントで表示するブロックを追加 |
| i18nファイルの作成 | `config/locales/ja.yml` | 下記の全キーを定義 |
| flash種別の統一 | 各コントローラー | `notice` / `alert` / `success` / `danger` の使い分けを統一し、viewと対応させる |
| 未実装flashの追加 | `UsersController`, `UserSessionsController`, `TipsController`, `ProfilesController` | 失敗時・成功時のflashを全アクションに追加 |
| 自動消去（任意） | Stimulus controller | 数秒後にフェードアウトするアニメーションを追加 |

---

### 定義が必要なi18nキー（`config/locales/ja.yml`）

```yaml
ja:
  defaults:
    flash_message:
      require_login: "ログインしてください"
  users:
    create:
      success: "アカウントを作成しました"
      failure: "アカウントの作成に失敗しました"
  user_sessions:
    create:
      success: "ログインしました"
      failure: "メールアドレスまたはパスワードが正しくありません"
    destroy:
      success: "ログアウトしました"
  tips:
    create:
      success: "Tipsを投稿しました"
      failure: "Tipsの投稿に失敗しました"
  profiles:
    update:
      success: "プロフィールを更新しました"
      failure: "プロフィールの更新に失敗しました"
```

---

### flash種別とdaisyUIアラートのマッピング

| flash種別 | daisyUIクラス | 用途 |
|---|---|---|
| `success` | `alert-success` | 正常完了（投稿・更新・ログイン等） |
| `notice` | `alert-info` | 案内・情報（既存のnoticeを移行） |
| `alert` | `alert-warning` | 注意 |
| `danger` | `alert-error` | エラー・ログイン必須リダイレクト等 |

---

## 3. 対応優先順位

| 優先度 | 対象 | 理由 |
|---|---|---|
| 高 | flashメッセージの表示実装 + `ja.yml`作成 | 現状ユーザーに何も伝わっていないため最優先 |
| 高 | ヘッダー（ログイン前後） | 全ページ共通。ナビゲーション導線に直結 |
| 高 | ログイン・新規登録ページ | 認証フローの入口。見た目が最初の印象を決める |
| 中 | Tips投稿フォーム | コア機能。プレースホルダーで入力体験を向上 |
| 中 | Tips一覧・カードパーシャル | 最も頻繁に閲覧されるページ |
| 中 | Tips詳細ページ | ハードコードのauthor情報を動的に差し替え |
| 低 | プロフィール系 | Bootstrapを除去してTailwindに統一 |
| 低 | ランディングページ | デプロイ前に整備すれば十分 |
