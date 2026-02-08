
# Rails routes.rb の mount 記法とEngineルーティング

## はじめに

最近「gemの公式ドキュメントを読んで実装してください」系の課題に取り組む中で、ソースコードを深く読む練習をしています。

例えば `.per(30)` を使えば1ページにコンテンツ30個表示できることは理解できるけど、少し踏み込んで **「じゃあ、なぜ `per` メソッドでそれができるの？」** とソースコードを読み解く部分に挑戦中です。

方法は技術面談で教わった、**GitHubのリポジトリをクローンして、Claude Codeで理解の壁打ちやファイル検索をしてもらう** というやり方です。

その一環として今日は、gem `letter_opener_web` について以下の疑問から少し深掘りしてみました。
まだまだ未熟ですが、少しずつもっと深くできたらなと思います。

> 余談ですが、いつもファイルを探るときは攻殻機動隊の少佐の気分です。

---

## Q: `mount` はなぜあの書き方になるのか？

```ruby
mount LetterOpenerWeb::Engine, at: "/letter_opener"
#     ^^^^^^^^^^^^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^
#     使いたいRackアプリ              このURLになると左のRackアプリが実行
```

## 具体的な流れ

例）ブラウザ: `GET /letter_opener/abc123/plain`

1. **Railsルーター**: `/letter_opener` で始まる → Engineに委譲
2. **Engine側が受け取るのは**: `/abc123/plain`（`/letter_opener` 部分が外される）
3. Engineの `routes.rb` で `':id(/:style)'` にマッチ
4. `LettersController#show` が実行される

> **ポイント**: `at:` のパスがプレフィックスとして剥がされてからEngine内部のルーティングに渡る

## Q: プレフィックスが外されるとは？

`at: xxxx` 部分がなくなり、`/abc123/plain` のみがEngine側の `config/routes.rb` に渡る。

## Engine側のルーティング定義

ファイルを確認してみると実際に同様に `config.rb` がある。以下はカリキュラムでよくみる書き方だった。

```ruby
LetterOpenerWeb::Engine.routes.draw do
  get  '/',                     to: 'letters#index',      as: :letters
  post 'clear',                 to: 'letters#clear',      as: :clear_letters
  get  ':id(/:style)',          to: 'letters#show',       as: :letter
  post ':id/delete',            to: 'letters#destroy',    as: :delete_letter
  get  ':id/attachments/:file', to: 'letters#attachment',  constraints: { file: %r{[^/]+} }
end
```
