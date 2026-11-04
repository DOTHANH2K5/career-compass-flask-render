# Career Compass — キャリア方向性ガイド

AIや自動化によって仕事の内容が変化する時代に、自分の経験・興味を整理し、次のキャリアの選択肢を考えるためのFlaskアプリです。

## 主な機能

- 現在の職業・興味・経験・目標を入力して簡易診断
- 職業に含まれる「自動化されやすい定型業務」の例を表示
- 人間の判断・対人能力などを活かしやすい業務例を表示
- 学習候補スキル、キャリア候補、次の行動ステップを提案
- 外部APIキー・有料API不要

> 注意：表示する自動化スコアは、職業そのものがなくなる確率ではありません。一般的な業務例をもとにした学習用の目安です。実際の影響は会社、地域、業務内容、経験によって異なります。転職や学習の判断では、最新の求人情報や公的な職業情報も確認してください。

## ファイル構成

```text
career-compass/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    ├── style.css
    └── app.js
```

## ローカルで実行

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS / Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
python app.py
```

ブラウザで http://127.0.0.1:5000 を開きます。

## Renderで公開

- Environment: `Python`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

`render.yaml`を使う場合、Renderが設定を読み込みます。GitHubにpushした後、RenderでNew → Web Serviceからリポジトリを接続してください。

## 技術構成

- Python / Flask
- HTML / Jinja2
- CSS
- JavaScript（入力補助・文字数表示）
- 診断ロジックはPython内のルールベース処理
