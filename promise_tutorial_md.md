# Promiseで非同期処理を制御してみよう

**目安時間**: 3時間  
**必須**

## 概要

JavaScriptはシングルスレッドで動作するため、時間のかかる処理を同時に実行すると、ユーザーインターフェースが固まってしまう可能性があります。そのため、非同期処理は非常に重要な概念になります。

本カリキュラムでは、JavaScriptの非同期処理を制御するためのPromiseの基本的な使い方を学びます。

## このカリキュラムのゴール

- Promiseの基本的な使い方を理解していること
- Promiseを使った非同期処理の流れを理解していること
- Promiseチェーンを使った非同期処理の流れを理解していること
- Promise.allとPromise.raceを使った複数の非同期処理の流れを理解していること

## 完成形スクリーンショット

![完成形](Image from Gyazo)

ブラウザのコンソールでPromiseを使った非同期処理の結果を確認できるようになります。コンソールに表示される処理の順序を通じて、非同期処理の流れとPromiseの動作を理解することができます。

## AI活用の心得 - 今回のポイント -

AIは「コードを理解するサポート」として非常に役立ちます。コードの解説を依頼したり、自分の理解をAIに説明して正しいかどうか確認したりすることで、理解を深めることができます。

### AI講師に聞く際のプロンプト例

AIを「学習のパートナー」として活用すれば、コードの読み解きがぐっと楽になります。さまざまな聞き方を試しながら、より良い出力を得られる方法を探してみましょう。

さらに、応用STEPを見据えた学習法として、AIに質問する前後で公式リファレンスや技術記事を読むと、理解が一層深まり、学習効果が高まります。

## 説明

Promiseは、JavaScriptの非同期処理を扱いやすくするためのオブジェクトです。Promiseは「約束」を意味しており、非同期処理の結果が「成功」または「失敗」したときに、その結果を通知するための仕組みになります。

Promiseは常に以下の3つの状態を持っています。

- **Pending(保留中)**: 初期状態。非同期処理がまだ完了していない状態。
- **Fulfilled(成功)**: 非同期処理が完了した状態。`resolve()`が呼ばれたとき。
- **Rejected(失敗)**: 非同期処理が失敗した状態。`reject()`が呼ばれたとき。

これらの状態が変化することで、非同期処理の流れを制御することができます。状態の変化は一方通行であり、PendingからFulfilledまたはRejectedに遷移した後は、再度Pendingに戻ることはありません。

### Promiseの基本的な流れ

1. 非同期処理を開始すると、Promiseオブジェクトが作成されます。状態はPendingになります。
2. 処理が成功すると、`resolve()`が呼ばれ、状態がFulfilledに変わります。
3. 処理が失敗すると、`reject()`が呼ばれ、状態がRejectedに変わります。
4. 状態がFulfilledになった場合は、`then()`メソッドが呼ばれ、成功時の処理が実行されます。
5. 状態がRejectedになった場合は、`catch()`メソッドが呼ばれ、失敗時の処理が実行されます。

## 事前準備

このカリキュラムでは、ブラウザのコンソールを使ってJavaScriptの非同期処理とPromiseの動作を確認します。事前に開発環境を準備しましょう。

### 準備内容

任意のディレクトリに移動し、`promise-js`ディレクトリを作成し、`index.html`と`script.js`を作成してください。

```bash
$ mkdir promise-js
$ cd promise-js
$ touch index.html script.js
```

### 準備内容

`index.html`に下記のコードを書いてください。

```html
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>JavaScript基礎 Promiseで非同期処理を制御してみよう</title>
    <script src="script.js"></script>
  </head>
  <body>
  </body>
</html>
```

ブラウザで表示して、検証ツールのコンソールを開きます。

```bash
$ open -a 'Google Chrome' index.html
```

## 説明

まず、JavaScriptの非同期処理の流れを確認してください。

`script.js`に下記のコードを記載してください。

```javascript
console.log("処理開始");

// setTimeout()を使った非同期処理(2秒後に実行)
setTimeout(() => {
  console.log("非同期処理完了");
}, 2000);

console.log("処理終了");
```

ブラウザをリロードして、コンソールを確認してください。

表示される順番は以下のようになります。

```
処理開始
処理終了
非同期処理完了
```

`setTimeout`内の処理は2秒後に実行されるため、「非同期処理完了」よりも先に「処理終了」が表示されます。

このように、JavaScriptは非同期処理を行う際に、他の処理をブロックせずに実行することができます。

## 説明

次に、Promiseを使って非同期処理を制御する基本的な書き方を確認していきます。

### 成功時の処理

`script.js`を以下のように変更してください。

```javascript
console.log("処理開始");

// Promiseを使った非同期処理
const myPromise = new Promise((resolve, reject) => {
  // 非同期処理(2秒後に成功)
  setTimeout(() => {
    resolve("成功しました!");
  }, 2000);
});

// Promiseの結果を処理
myPromise
  .then((result) => {
    console.log("Promiseの結果:", result);
  })
  .catch((error) => {
    console.error("Promiseのエラー:", error);
  })
  .finally(() => {
    console.log("Promiseの処理が完了しました");
  });

console.log("処理終了");
```

ブラウザをリロードして、コンソールを確認してください。

表示される順番は以下のようになります。

```
処理開始
処理終了
Promiseの結果: 成功しました!
Promiseの処理が完了しました
```

### 失敗時の処理

次に、Promiseを使った非同期処理が失敗した場合の処理を確認します。

`script.js`を以下のように変更してください。

```javascript
console.log("処理開始");

// Promiseを使った非同期処理(失敗パターン)
const myPromise = new Promise((resolve, reject) => {
  // 非同期処理(2秒後に失敗)
  setTimeout(() => {
    reject(new Error("処理が失敗しました"));
  }, 2000);
});

// Promiseの結果を処理
myPromise
  .then((result) => {
    console.log("Promiseの結果:", result);
  })
  .catch((error) => {
    console.error("Promiseのエラー:", error.message);
  })
  .finally(() => {
    console.log("Promiseの処理が完了しました");
  });

console.log("処理終了");
```

ブラウザをリロードして、コンソールを確認してください。

表示される順番は以下のようになります。

```
処理開始
処理終了
Promiseのエラー: 処理が失敗しました
Promiseの処理が完了しました
```

このように、成功時には`then()`メソッドが呼ばれ、失敗時には`catch()`メソッドが呼ばれます。`finally()`メソッドは、成功・失敗に関わらず必ず実行される処理を記述するために使用します。

## 説明

Promiseの特徴として、複数の非同期処理を連結(チェーン)して実行することできる点があります。これにより、非同期処理の結果を次の処理に渡すことができます。

`script.js`を以下のように変更してください。

```javascript
console.log("処理開始");

// 数値を受け取って2倍にするPromise関数
function doubleAfter1Second(num) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(num * 2);
    }, 1000);
  });
}

// Promiseチェーンで連続処理
doubleAfter1Second(5)
  .then((result) => {
    console.log("最初の結果:", result); // 10
    return doubleAfter1Second(result); // 次のPromiseを返す
  })
  .then((result) => {
    console.log("2回目の結果:", result); // 20
    return doubleAfter1Second(result); // さらに次のPromiseを返す
  })
  .then((result) => {
    console.log("3回目の結果:", result); // 40
  })
  .catch((error) => {
    console.error("エラー発生:", error);
  });

console.log("処理終了");
```

上記のコードは、最初の数値を受け取って2倍にする非同期処理をPromiseチェーンで連続して実行しています。

ブラウザをリロードして、コンソールを確認してください。

表示される順番は以下のようになります。

```
処理開始
処理終了
最初の結果: 10
2回目の結果: 20
3回目の結果: 40
```

Promiseチェーンを使うことで、非同期処理の結果を次に渡すことができます。

このようにすることで、コールバック関数のネストが深くなってしまう「コールバック地獄」を避けることができます。

## 説明

実際の開発では、複数の非同期処理を同時に行い、全ての処理が完了したときに結果を取得したり、最初に完了した処理だけを取得したりすることがよくあります。

### Promise.all()

`Promise.all()`は、複数のPromiseを並行で実行し、全ての処理が完了したときに次の処理を実行するためのメソッドです。

`script.js`を以下のように変更してください。

```javascript
const promise1 = new Promise(resolve => setTimeout(() => resolve("結果1"), 1000));
const promise2 = new Promise(resolve => setTimeout(() => resolve("結果2"), 2000));
const promise3 = new Promise(resolve => setTimeout(() => resolve("結果3"), 1500));

console.log("Promise.all開始");

Promise.all([promise1, promise2, promise3])
  .then(results => {
    console.log("全ての結果:", results); // ["結果1", "結果2", "結果3"]
  })
  .catch(error => {
    console.error("いずれかでエラー:", error);
  });
```

上記のサンプルコードでは、3つのPromiseを同時に実行し、全てのPromiseが成功したときに結果を配列として取得しています。

ブラウザをリロードして、コンソールを確認し、以下のような順番で表示されることを確認してください。

```
Promise.all開始
全ての結果: ["結果1", "結果2", "結果3"]
```

### Promise.race()

`Promise.race()`は、複数のPromiseのうち、最初に処理を完了した結果だけを取得するためのメソッドです。

`script.js`を以下のように変更してください。

```javascript
const fast = new Promise(resolve => setTimeout(() => resolve("速い処理"), 1000));
const slow = new Promise(resolve => setTimeout(() => resolve("遅い処理"), 3000));

console.log("Promise.race開始");

Promise.race([fast, slow])
  .then(result => {
    console.log("最初の結果:", result); // "速い処理"
  });
```

上記のサンプルコードでは、2つのPromiseを同時に実行し、最初に完了したPromiseの結果だけを取得しています。

ブラウザをリロードして、コンソールを確認し、以下のような順番で表示されることを確認してください。

```
Promise.race開始
最初の結果: 速い処理
```

## まとめ

本カリキュラムでは、Promiseを使った非同期処理の基本的な流れを学びました。

- Promiseの基本的な使い方について学びました。
- Promiseの3つの状態(Pending, Fulfilled, Rejected)について学びました。
- JavaScriptにおける非同期処理の流れとPromiseの役割について学びました。
- Promiseチェーンを使った複数の非同期処理を連結して実行する方法について学びました。
- `Promise.all()`を使った全てのPromiseの結果を取得する方法について学びました。
- `Promise.race()`を使った最初に完了したPromiseの結果を取得する方法について学びました。