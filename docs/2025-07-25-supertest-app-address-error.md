## TL;supertest で app.address is not a function が出た

supertest で Express アプリをテストする際、`TypeError: app.address is not a function`エラーが発生。原因は server インスタンスではなく app インスタンスをエクスポートすべきところを間違えていたこと。適切なオブジェクトのエクスポートと環境条件分岐で解決。

## 背景と課題

Node.js バックエンドアプリケーションで Jest と supertest を使った認証機能のテストを実装している際、設定段階で躓きました。supertest は、Express アプリケーションに対して HTTP リクエストを送信してレスポンスをテストするライブラリです。一方、Jest は JavaScript 用のテスティングフレームワークで、テストの構造化と実行を担当します。

開発環境では通常通りサーバーが起動していたものの、テスト実行時に`TypeError: app.address is not a function`エラーが発生。このエラーは supertest が Express アプリケーションインスタンスを期待しているにも関わらず、異なるオブジェクト（この場合はサーバーインスタンス）を受け取った際に発生します。

## 事象の再現手順

問題が発生していたコード構成は以下の通りです：

```js
// server.js（修正前）
const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

// ミドルウェアとルート設定
app.use(express.json());
app.get("/api/test", (req, res) => {
  res.json({ message: "Test endpoint" });
});

const server = app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

module.exports = server; // ❌ 問題箇所
```

```js
// test/app.test.js
const request = require("supertest");
const app = require("../server");

describe("Authentication Tests", () => {
  test("GET /api/test should return test message", async () => {
    const response = await request(app).get("/api/test").expect(200);

    expect(response.body.message).toBe("Test endpoint");
  });
});
```

テスト実行時に以下のエラーが発生：

```
TypeError: app.address is not a function
    at Test.serverAddress (node_modules/supertest/lib/test.js:XX:XX)
```

## 解決までの思考プロセス

最初の仮説は「supertest 環境では app オブジェクトが必要だが、server.js でアプリとサーバーを同じファイルでコーディングしているからエラーが発生している」でした。

この仮説を検証するため、まず supertest のドキュメントを確認しました。supertest は`request(app)`の形で Express アプリケーションインスタンスを期待していることが判明。しかし、コードでは`module.exports = server`としてサーバーインスタンスをエクスポートしていました。

問題の核心は以下の点でした：

- supertest は Express アプリケーション（`app`）を必要とする
- エクスポートしていたのはサーバーインスタンス（`server`）
- テスト環境でもサーバーが起動してしまい、ポート競合の可能性

## 最終的な解決策

責任の分離とオブジェクトの適切なエクスポートで問題を解決しました：

```js
// app.js（新規作成）
const express = require("express");
const app = express();

// ミドルウェア設定
app.use(express.json());

// ルート定義
app.get("/api/test", (req, res) => {
  res.json({ message: "Test endpoint" });
});

module.exports = app; // ✅ appインスタンスをエクスポート
```

```js
// server.js（修正後）
require("dotenv").config();
const app = require("./app");
const port = process.env.PORT || 3000;

// テスト環境以外でのみサーバー起動
if (process.env.NODE_ENV !== "test") {
  app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
  });
}

module.exports = app; // ✅ appインスタンスをエクスポート
```

解決のポイントは 3 つです：

**適切なオブジェクトのエクスポート** - server インスタンスから app インスタンスに変更し、supertest が期待する Express アプリケーションを提供しました。

**環境による条件分岐** - `NODE_ENV=test`の時はサーバー起動をスキップし、テスト実行時の不要なサーバー起動を防止しました。

**責任の分離の維持** - app.js でアプリケーションロジック、server.js でサーバー起動とテスト用エントリーポイントを分離しました。

## 他プロジェクトでの応用可能性

この解決パターンは Express + supertest を使用する多くのプロジェクトで応用可能です。特にマイクロサービスアーキテクチャや CI/CD 環境では、アプリケーションとサーバー起動の分離が重要になります。

body-parser の設定や Express 5 への移行時にも同様の JSON error が発生する可能性があります。Express 5 では内蔵の JSON パーサーがより厳密になっているため、適切なエラーハンドリングと組み合わせることで堅牢なテスト環境を構築できます。

似たような課題を解決した OSS プロジェクトとして、[Express 公式のテストパターン](https://expressjs.com/en/guide/testing.html)や[Jest 公式ドキュメント](https://jestjs.io/docs/testing-frameworks)が参考になります。特に Next.js や Nuxt.js などのフルスタックフレームワークでも、API ルートのテスト時に同様のパターンが使用されています。
