# 1. まず作るもの（最小構成）

## 置き場所（どっちでもOK）

- プロジェクト専用にしたい → `<workspace-root>/.agent/skills/`
- 全プロジェクト共通にしたい → `~/.gemini/antigravity/skills/`

## ディレクトリ構造（例）

```
rails-official-doc-matrix/
├── SKILL.md
├── references/
│   ├── sources.yml
│   └── output_template.md
└── scripts/
    └── build_table.py   (任意)
```

この構造自体が公式に例示されています（SKILL.md + scripts + references）。

# 2. SKILL.md に書くべき“自動化したいプロセス”の中身

公式スキル仕様では、SKILL.md は **YAML Frontmatter（ルータが参照）** と **Markdown Body（実行手順）** に分かれます。  
description が「いつ使うか」のトリガーになります。

## SKILL.md（コピペで動く骨格）

```md
---
name: rails-official-doc-matrix
description: Rails機能実装の前に、一次情報（公式ドキュメント/ガイド/API）を調査し、章タイトルを明示して「背景/理由付きの参照表（Markdown表）」を自動生成する。N+1/includes/association/migration/routing等の調査にも使う。
---

# Rails Official Doc Matrix

## Goal
ユーザーが指定した機能領域（例: ブックマーク、N+1、認証）について、
1) 公式一次情報を特定し
2) ドキュメント上の章タイトルをそのまま明示し
3) 「なぜ読むべきか（背景/理由）」とセットで
4) Markdownの表として出力する。

## Inputs (ask only if missing)
- Rails version (例: 7.0.3.1)
- 対象領域（例: includesのN+1、bookmark）
- 想定モデル（例: User/Post/Bookmark）や画面（任意）

## Instructions
1. まず「そのドキュメントに該当機能の直接記載があるか」を確認する。
   - ない場合は「直接記載なし」と明言し、前提として必要な章に切り替える（例: REST/Associations/Migrations 等）。
2. 参照ソースは原則として以下の公式のみ：
   - guides.rubyonrails.org
   - api.rubyonrails.org
   - edgeguides は version 差分が必要な時だけ（使ったら明記）
3. 各リサーチ項目ごとに、必ず「章タイトル（ドキュメント表記どおり）」を記載する。
4. 出力は references/output_template.md の列構成に合わせる。
5. 余計な実装コードは書かない。目的は「理解を深めるための参照表」。

## Constraints
- 公式以外（ブログ等）は “補足” でのみ使用し、一次情報扱いしない。
- 章タイトルが曖昧な場合は、該当ページで見出しを再確認する。
- 破壊的操作（rm -rf、DB削除等）の提案は禁止。

## Optional Automation
- scripts/build_table.py がある場合はそれを使って表を整形してよい。
```

# 3. “機械化”しやすい部分を scripts/ に寄せる

Skill は scripts/ を同梱でき、SKILL.md から相対パスで呼べます。  
あなたのユースケースだと **「公式ページから見出し（章タイトル）を抜く」** が一番自動化の旨みです。

## 例: references/sources.yml（調査対象の公式ソースを固定）

```yml
rails_version: "7.0.3.1"
primary_sources:
  - name: "Rails Guides"
    base: "https://guides.rubyonrails.org/"
  - name: "Rails API"
    base: "https://api.rubyonrails.org/"
```

## 例: references/output_template.md（表の列を固定）

```md
| リサーチ項目 | 一次情報（公式） | 該当箇所（章タイトル） | 背景/理由 | 紙に書く要点 |
|---|---|---|---|---|
```

## 例: scripts/build_table.py（超シンプルな整形。入力JSON→表）

```py
import json

def md_escape(s: str) -> str:
    return s.replace("|", "\\|").strip()

data = json.load(open("input.json", "r", encoding="utf-8"))

print("| リサーチ項目 | 一次情報（公式） | 該当箇所（章タイトル） | 背景/理由 | 紙に書く要点 |")
print("|---|---|---|---|---|")
for row in data["rows"]:
    print("| " + " | ".join(md_escape(row[k]) for k in [
        "topic","source","section","reason","paper"
    ]) + " |")
```

# 4. Antigravity 側の設定（安全に自動化するコツ）

Skill は必要に応じてスクリプト実行やブラウズを伴うので、安全柵を先に立てるのが吉です。

## ターミナル実行は「都度レビュー」にしておく（自動実行を避ける）

Antigravity には Terminal Execution policy の設定があり、実行前に承認させる運用にできます。

## ブラウズ先を公式ドメインに寄せる

Browser URL Allowlist を設定して、信頼ドメインだけに絞れます（allowlistファイルの場所も公式に記載あり）。  
例：`guides.rubyonrails.org`, `api.rubyonrails.org`

# 5. 実際の使い方（呼び出しプロンプトの型）

Skill が拾いやすいのは、description に書いた語彙が入っているときです。なので会話ではこう呼ぶと安定します。

例）
「Rails 7.0.3.1。includes の N+1 を理解したい。一次情報（公式）を章タイトル明示で表にまとめて。背景/理由も付けて。」

# 6. 仕上げの一工夫（あなたの“プロ”っぽい運用にする）

## “領域別チェックリスト”を references/ に貯める

例：references/rails_topics.yml に「N+1なら Query Interface の Eager Loading を必ず入れる」みたいなルールを保存

## 出力を必ず同じ列・同じ順番に固定

初学者向けカリキュラムは “型” が命。表の列をテンプレで固定すると教材として再利用しやすい
