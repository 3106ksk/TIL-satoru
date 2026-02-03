# ActiveRecord::RecordNotFound in PostsController#show

Created: January 15, 2026 7:42 AM
Updated: January 15, 2026 11:57 AM

## 相談/知りたいこと：

デバッグを行うときの思考プロセス。

最初どの範囲からチェックするのか、どこをチェックするべきなのか分からず戸惑ってしまうことがある

## カリキュラム：

エラーへの向き合い方と解決方法/**エラーの情報を見てバグを解消しよう**

## 前提：以下のデバッグツールを使ったバグの解決

デバッグツール：

- gem 'debug
- Rspec

Rspec からのスクリーンショット

![Screenshot 2026-01-15 at 11.01.53 AM.png](<ExportBlock-997ed837-35d3-4b39-a462-584cefc2226e-Part-1/ActiveRecord RecordNotFound in PostsController#sho/Screenshot_2026-01-15_at_11.01.53_AM.png>)

該当コード

```jsx
respond_to do |format|
  format.html do
    binding.break
    @post = current_user.posts.find(params[:id])
  end
end
```

🤖 ログ：Couldn't find Post with 'id'=33 [WHERE "posts" "user_id" = $1]

🤔 ログから読み取ったこと：user 1 に post id 33 が見つからない

エラー原因：

Post #show アクションは全ユーザーの該当する投稿を見る処理なのに、current_user(ログイン)ユーザーの user_id と post id が両方マッチする条件のみを find していた

> 以下の思考とデバッグプロセスで上記のエラー原因に辿り着いたが、実務での場合、同様のエラーに取り組むときのデバッグや思考プロセスについて知りたい。また以下のプロセスでの改善点についてあれば知りたい

## 🤔 思考/デバッグプロセス：

- このエラーログから binding.break をどこにおくのかを判断するには？？
- fortmat の中身を確認することで適切な id があるかを知る？

<aside>
💡

### 仮説１：format.html はクラインアントサイドのフォームから送られた、フォームについての情報を持つオブジェクト？そして、format.html do で オブジェクトの中にある id を利用して find で db から該当データを探しているという処理であっている？

➡️format について再度調べる

</aside>

❌format.html が何か曖昧

正しい理解：

- format.html はクライアントから送信された ulr の形式に応じて view に返すフォーマットを html か json 形式かをしている。
- params:id はリクエスト時の url に格納してある id を受け取る

➡️ 該当コードの直前に binding.break で変数などを確かめる

```jsx
=>#0    block in show (2 levels) at /myapp/app/controllers/posts_controller.rb:14
  #1    ActionController::MimeResponds#respond_to(mimes=[]) at /usr/local/bundle/gems/actionpack-7.2.1/lib/action_controller/metal/mime_responds.rb:224
  # and 79 frames (use `bt' command for all frames)
(ruby:remote) current_user&.id
3
(rdbg:remote) p params[:id]    # command
=> "39"
(rdbg:remote) p Post.exists?(39)    # command
=> false
```

🤔 疑問１：db が存在しないのになぜ、UI としてみれているの？？

そもそも、Post #show アクションは全ユーザーの該当する投稿を見ることができるアクション

<aside>
💡

仮説２：current_user(ログイン)ユーザーが持つ post_id(投稿)のみで find を実行している設計がおかしいのでは？？

</aside>

Post.find で posts テーブル全体から探す設計に変更

```jsx
      format.html do
        @post = Post.find(params[:id])
      end
```

```jsx
Post.find
SELECT "posts".*
FROM "posts"
WHERE "posts"."id" = 33
LIMIT 1;

current_user.posts.find(params[:id])
SELECT "posts".*
FROM "posts"
WHERE "posts"."user_id" = 1   -- current_user.id
  AND "posts"."id" = 33
LIMIT 1;
```
