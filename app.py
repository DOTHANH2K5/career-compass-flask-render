import os
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "career-compass-local-dev-key")

# This is a transparent, rule-based guide, not a scientific forecast.
# Scores describe exposure of common tasks to automation, not the likelihood
# that a person will lose their job.
JOB_DATA = {
    "事務・一般事務": {
        "exposure": 78,
        "automatable": ["定型的なデータ入力", "書類の分類・転記", "定型メールの作成"],
        "human": ["例外対応", "関係者との調整", "業務フローの改善"],
        "skills": ["Excel・スプレッドシート活用", "業務改善", "データ確認・品質管理"],
        "paths": ["業務改善アシスタント", "営業事務＋データ管理", "カスタマーサポート"]
    },
    "販売・接客": {
        "exposure": 42,
        "automatable": ["在庫・売上の定型集計", "セルフレジでの会計", "よくある質問への一次回答"],
        "human": ["顧客の希望をくみ取る接客", "クレーム・例外対応", "売場づくり・提案"],
        "skills": ["傾聴・提案力", "商品知識の発信", "EC・SNS運用"],
        "paths": ["カスタマーサクセス", "EC運営アシスタント", "法人営業"]
    },
    "製造・工場": {
        "exposure": 57,
        "automatable": ["反復的な組立・検査", "定型的な記録入力", "単純な搬送作業"],
        "human": ["設備の異常判断", "品質改善", "安全管理・チーム連携"],
        "skills": ["機械・設備の基礎知識", "品質管理", "データ記録・分析"],
        "paths": ["設備保全", "品質管理", "生産管理アシスタント"]
    },
    "運転・物流": {
        "exposure": 48,
        "automatable": ["配送ルートの最適化", "荷物の仕分け支援", "配送状況の自動通知"],
        "human": ["現場での安全判断", "顧客・現場との調整", "想定外への対応"],
        "skills": ["物流管理システム", "安全・法令知識", "在庫・配送データ管理"],
        "paths": ["物流管理", "配車・運行管理補助", "倉庫オペレーション改善"]
    },
    "営業": {
        "exposure": 38,
        "automatable": ["見込み顧客リストの整理", "定型提案書の下書き", "営業記録の入力"],
        "human": ["信頼関係づくり", "課題の発見", "交渉・提案の調整"],
        "skills": ["課題ヒアリング", "CRM活用", "データに基づく提案"],
        "paths": ["法人営業", "カスタマーサクセス", "営業企画アシスタント"]
    },
    "デザイン・クリエイティブ": {
        "exposure": 55,
        "automatable": ["ラフ案の大量生成", "画像の簡単な加工", "定型バナー制作"],
        "human": ["ブランド理解", "コンセプト設計", "目的に合わせた表現の判断"],
        "skills": ["デザイン基礎", "ユーザー理解", "AIツールの編集・評価"],
        "paths": ["UIデザイン補助", "Webコンテンツ制作", "マーケティングクリエイティブ"]
    },
    "IT・エンジニア": {
        "exposure": 50,
        "automatable": ["定型コードの補完", "テストコードの下書き", "簡単な技術文書の作成"],
        "human": ["要件整理", "設計判断", "セキュリティ・品質への責任"],
        "skills": ["基礎プログラミング", "問題分解", "テスト・セキュリティ"],
        "paths": ["Web開発", "QA・テストエンジニア", "社内ITサポート"]
    },
    "医療・介護・福祉": {
        "exposure": 25,
        "automatable": ["記録の下書き", "シフト・事務作業の補助", "情報検索"],
        "human": ["相手の状態に応じたケア", "信頼関係づくり", "倫理的な判断"],
        "skills": ["専門資格・知識", "観察・記録", "多職種連携"],
        "paths": ["専門性を深める", "医療・介護事務", "福祉用具・支援サービス"]
    },
    "教育": {
        "exposure": 32,
        "automatable": ["教材案の作成", "小テストの採点補助", "学習進捗の集計"],
        "human": ["学習者の動機づけ", "理解度に応じた指導", "保護者・関係者との連携"],
        "skills": ["個別支援", "教材設計", "デジタル学習ツール"],
        "paths": ["教育コンテンツ制作", "学習支援", "研修・人材育成"]
    },
    "その他・まだ決めていない": {
        "exposure": 45,
        "automatable": ["定型入力・集計", "繰り返しの情報整理", "定型的な文章作成"],
        "human": ["状況に応じた判断", "対人コミュニケーション", "新しい課題への対応"],
        "skills": ["デジタル基礎力", "情報整理", "伝える力"],
        "paths": ["カスタマーサポート", "業務サポート", "Web・デジタル分野の初級職"]
    },
}

INTEREST_PATHS = {
    "人と話す・支える": ["カスタマーサクセス", "カスタマーサポート", "人材・キャリア支援"],
    "調べる・分析する": ["データ分析アシスタント", "品質管理", "マーケティング分析補助"],
    "ものを作る・表現する": ["Webコンテンツ制作", "UIデザイン補助", "Web開発"],
    "仕組みを整える": ["業務改善アシスタント", "社内ITサポート", "生産・物流管理"],
    "体を動かす・現場で働く": ["設備保全", "物流管理", "介護・福祉の専門職"],
    "まだ分からない": ["事務・業務サポート", "カスタマーサポート", "デジタル基礎学習から始める"]
}

def make_recommendations(job, interest, skills, goal):
    data = JOB_DATA[job]
    candidates = list(data["paths"]) + INTEREST_PATHS[interest]
    # Keep order while removing duplicates.
    unique = list(dict.fromkeys(candidates))
    return unique[:4]

def analyze(form):
    job = form.get("current_job", "その他・まだ決めていない")
    if job not in JOB_DATA:
        job = "その他・まだ決めていない"
    interest = form.get("interest", "まだ分からない")
    if interest not in INTEREST_PATHS:
        interest = "まだ分からない"
    data = JOB_DATA[job]
    exposure = data["exposure"]
    level = "高め" if exposure >= 65 else ("中程度" if exposure >= 40 else "比較的低め")
    return {
        "name": form.get("name", "").strip() or "あなた",
        "job": job,
        "interest": interest,
        "experience": form.get("experience", "これから経験を積みたい"),
        "skills_input": form.get("skills", "").strip(),
        "goal": form.get("goal", "方向性を見つけたい"),
        "exposure": exposure,
        "level": level,
        "automatable": data["automatable"],
        "human": data["human"],
        "skills": data["skills"],
        "paths": make_recommendations(job, interest, form.get("skills", ""), form.get("goal", "")),
        "steps": [
            f"現在の経験から「{data['human'][0]}」に関する具体例を3つ書き出す",
            f"「{data['skills'][0]}」を小さな課題で練習し、成果物を1つ作る",
            "興味のある職種を2〜3件調べ、必要スキルと求人条件を比較する",
            "学んだこと・成果物・経験を履歴書やポートフォリオにまとめる"
        ]
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", jobs=list(JOB_DATA.keys()), interests=list(INTEREST_PATHS.keys()))

@app.route("/diagnosis", methods=["POST"])
def diagnosis():
    result = analyze(request.form)
    return render_template("result.html", result=result)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
