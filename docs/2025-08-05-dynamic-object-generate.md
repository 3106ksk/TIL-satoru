# オブジェクト引数を使った柔軟なユーザーオブジェクトの動的生成の仕組み

## 1. コンテキスト
- **フレームワーク / ライブラリ**: Jest + Supertest + Node.js + Sequelize
- **ゴール（何を実装したかったか）**: 複数ユーザーが関わるAPIエンドポイントのテスト（データ分離、権限制御等）を効率的に実装したかった

## 2. 発生した問題

| 時刻  | 現象 | エラーメッセージ |
|-------|------|------------------|
| 14:30 | 複数ユーザーのテストで2回目のユーザー作成が失敗 | `Validation error: email must be unique` |
| 14:35 | 固定ユーザーでは他ユーザーとの分離テストができない | テストケースが実装不可能 |

## 3. 仮説と検証

| 仮説 | 検証手順 | 結果 |
|------|----------|------|
| 固定値でユーザー作成しているため重複エラー | `createTestUser()`の実装を確認 | ✅ 毎回同じemail/usernameを使用していた |
| 引数を受け取れるようにすれば解決 | オブジェクト引数に変更してテスト | ✅ 異なるユーザーの動的作成が可能になった |
| 分割代入でデフォルト値も設定できる | `const { email = 'default' } = options`で検証 | ✅ 柔軟性とデフォルト値の両立が実現 |

## 4. 根本的な原因/知識のギャップ
- **引数設計の理解不足**: 固定値の関数しか作れず、パラメーター化の発想がなかった
- **JavaScriptの分割代入とデフォルト値の活用方法**: オブジェクト引数パターンの知識不足
- **テスト設計の考え方**: 「1つの関数で複数のバリエーションを作る」という設計思想の欠如

## 5. 学んだこと

```javascript
// Before: 固定値で再利用不可
global.createTestUser = async () => {
 return await User.create({
   email: 'test@example.com'  // 常に同じ値
 });
};

// After: オブジェクト引数で柔軟性を実現
global.createTestUser = async (options = {}) => {
 const { 
   email = 'test@example.com',
   username = 'testuser' 
 } = options;
 
 return await User.create({ email, username });
};