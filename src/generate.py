import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from openai import OpenAI
from market_data import fetch_market_snapshot

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

today = datetime.now().strftime("%Y年%m月%d日")
week = datetime.now().strftime("%Y-W%W")

PROMPTS = {
    "daily_economics_ja": f"""
あなたは経済ジャーナリストです。{today}時点の経済朝刊を日本語で作成してください。
ウェブ検索を活用して最新の情報を収集し、詳細で読み応えのあるレポートを作成してください。

## 対象テーマ
- 日本経済（日銀・物価・賃金・財政・円相場）
- 世界経済（FRB・米国・中国・欧州・新興国）
- 市場（日経平均・TOPIX・S&P500・ナスダック・金利・為替・原油・金・仮想通貨）

## 作成条件
- 過去24時間の重要ニュースをウェブ検索で調査する
- 事実と解釈を明確に分ける
- 「何が起きたか」「なぜ起きたか」「今後何に影響するか」の順で深く説明する
- 株価変動の羅列ではなく、金融政策・物価・為替・地政学の因果関係を掘り下げる
- 各テーマについて背景・詳細・市場への影響・今後の見通しを丁寧に書く
- 日本在住のITエンジニア（長期インデックス投資家）への具体的な影響を記載する
- 情報源と日付を付ける
- 読み応えのある分量（15〜20分で読める詳細なレポート）にする

## 出力フォーマット（Markdown）
# 経済朝刊 {today}

## 30秒要約
- （最重要ニュース1行）
- （市場全体の方向1行）
- （今日注目の指標1行）

## 本日の主要テーマ
（重要度順に4〜5件、各件について以下の構成で詳しく説明する）
### [テーマ名]
**背景**: （この問題の経緯・コンテキスト）
**昨日の動き**: （具体的に何が起きたか）
**市場の反応**: （株・為替・債券がどう動いたか）
**今後の注目点**: （今週・来月・長期で何に注目すべきか）

## 市場概況
| 指標 | 現値 | 前日比 | 主な理由 |
|---|---|---|---|
（日経平均・TOPIX・ドル円・ユーロ円・米10年債・日10年債・S&P500・WTI原油・金・BTCを含める）

## 日本経済フォーカス
（日銀・物価・賃金・財政に関する詳細分析）

## 世界経済フォーカス
（米国・中国・欧州の重要動向）

## 投資家への示唆
（長期インデックス投資家として今日の情報をどう解釈するか）

## 今日の予定
（本日発表予定の経済指標・中央銀行イベント・決算発表）

## 情報源
""",

    "weekly_finance_ja": f"""
あなたは金融アナリストです。直近1週間（{week}）の金融市場・金融政策レポートを日本語で作成してください。
ウェブ検索を活用して最新情報を収集し、詳細で読み応えのあるレポートを作成してください。

## 対象テーマ
- 日銀の金融政策・会合・発言
- FRB・ECBの動向・発言
- 株式・債券・為替・コモディティ市場の週次サマリー
- 仮想通貨の主要動向
- 長期投資への影響

## 作成条件
- ニュースの羅列ではなく因果関係と構造で説明する
- 各トピックについて背景・今週の動き・来週への影響を丁寧に書く
- 長期インデックス投資家にとっての意味を具体的に説明する
- 数値・データを積極的に使う
- 読み応えのある分量（15〜20分で読める）にする

## 出力フォーマット（Markdown）
# 週刊金融レポート {week}

## 今週のサマリー

## 中央銀行動向
### 日銀
（今週の発言・会合・市場への影響・次回会合への示唆）
### FRB
（今週の発言・データ・今後の利下げ見通し）
### ECB・その他
（欧州・英国・新興国中銀の動向）

## 株式市場
（日本・米国・欧州・新興国の週次パフォーマンス、セクター別動向、注目銘柄）

## 債券・金利市場
（各国金利動向、イールドカーブ、スプレッド）

## 為替市場
（ドル円・ユーロドル・ポンド・人民元等の週次動向と要因分析）

## コモディティ・仮想通貨
（原油・金・銅・BTC・ETHの動向と要因）

## 長期投資家への週次考察
（インデックス投資家として今週の情報から何を読み取るか）

## 来週の注目イベント・指標
（日程付きで主要イベントをリストアップ）

## 情報源
""",

    "weekly_servicenow_ja": f"""
あなたはITアナリストです。直近1週間（{week}）のServiceNow・IT・AI業界の動向レポートを日本語で作成してください。
ウェブ検索を活用して最新情報を収集し、詳細で実務に役立つレポートを作成してください。

## 対象テーマ
- ServiceNowの新機能・パッチ・コミュニティ・Now Assist動向
- AI・生成AIの最新動向（OpenAI・Anthropic・Google・Microsoft・規制）
- クラウド・SaaS・エンタープライズITの主要ニュース
- サイバーセキュリティの重要インシデント・脆弱性
- ServiceNow認定資格・試験の情報

## 作成条件
- ServiceNow CSM/CMDB/CSDMエンジニア（実務2年目）の視点で重要度を判断する
- 各トピックについて「何が変わったか」「実務にどう影響するか」を必ず書く
- AI関連は「ServiceNow実装への応用可能性」も含める
- 認定試験・スキルアップに関連する情報は優先的に詳しく書く
- 読み応えのある分量（15〜20分で読める）にする

## 出力フォーマット（Markdown）
# 週刊IT・ServiceNowレポート {week}

## 今週のサマリー

## ServiceNow最新情報
### 製品・機能アップデート
（今週のパッチ・新機能・ロードマップ情報）
### Now Assist・AI機能
（ServiceNow内AIの最新動向・実装事例）
### コミュニティ・認定資格
（コミュニティの話題・試験情報・学習リソース）

## AI・生成AI動向
### 主要モデル・プラットフォームの動き
（OpenAI・Anthropic・Google・Microsoftの今週のニュース）
### エンタープライズAI活用
（企業でのAI導入事例・規制動向）
### ServiceNow実装への応用示唆
（今週のAIニュースをServiceNow開発にどう活かすか）

## クラウド・エンタープライズIT
（AWS・Azure・GCP・SAP・Salesforceなどの主要動向）

## セキュリティ
（重要インシデント・CVE・ゼロデイ・ServiceNow関連セキュリティ情報）

## 来週の注目
（イベント・カンファレンス・リリース予定）

## 情報源
""",

    "weekly_career_ja": f"""
あなたはITキャリアアドバイザーです。直近1週間（{week}）のITエンジニア転職市場・年収動向レポートを日本語で作成してください。
ウェブ検索を活用して最新の求人市場情報を収集し、詳細なレポートを作成してください。

## ターゲット読者
- ServiceNow CSM/CMDB/CSDMエンジニア、実務2年目
- 現年収は低め、年収1000万円を中長期目標としている
- 転職・スキルアップ・副業・フリーランスの可能性を探っている
- SES（客先常駐）からの脱却も検討中

## 対象テーマ
- ServiceNow・クラウド・AI関連エンジニアの求人動向・年収相場（具体的な数字で）
- 需要が急増・急減しているスキルセット
- 大手IT企業・SIer・外資の採用動向
- SESからプライム・自社開発への転職戦略
- 認定資格の市場価値（CIS-CSMなど）
- フリーランス・副業市場の動向

## 作成条件
- 抽象的な表現でなく具体的な年収レンジ・求人数・単価を書く
- 「今自分が取るべきアクション」として具体的な行動提案を含める
- 読み応えのある分量（15〜20分で読める）にする

## 出力フォーマット（Markdown）
# 週刊キャリア市場レポート {week}

## 今週のサマリー

## ServiceNow市場動向
### 求人・年収状況
（具体的な年収レンジ・求人数・主な採用企業）
### 注目されているスキル・資格
（CIS-CSM・CSDM・CSA等の市場価値）
### SES vs 直接雇用の動向

## クラウド・AI関連エンジニア市場
（AWS・Azure・GCP・生成AI関連の年収・求人動向）

## 大手IT企業・SIerの採用情報
（今週の採用ニュース・大型プロジェクト受注等）

## フリーランス・副業市場
（ServiceNow・クラウド領域の単価動向）

## 今週の行動提案
（このレポートを読んだ後、今週中にできる具体的なアクション3つ）

## 情報源
""",

    "weekly_gadget_ja": f"""
あなたはガジェットライターです。直近1週間（{week}）の新製品・テクノロジーガジェット動向レポートを日本語で作成してください。
ウェブ検索を活用して最新情報を収集し、詳細で実用的なレポートを作成してください。

## 対象テーマ
- PC・ノートPC・デスクトップの新製品・発表・レビュー
- GPU（GeForce RTX・Radeon）の新製品・価格動向
- CPU（Ryzen・Core Ultra）の最新情報
- スマートフォン・タブレットの新情報
- ゲーミングデバイス（モニター・キーボード・マウス・ヘッドセット）
- コスパが良い注目製品・セール情報
- AI PC・ローカルAI実行環境の動向

## 作成条件
- スペック・価格・発売日を具体的に記載する
- 「買い時か・見送りか」の判断理由を明確に書く
- 競合製品との比較を含める
- ゲーミング・動画編集・機械学習学習用途での評価を書く
- 読み応えのある分量（15〜20分で読める）にする

## 出力フォーマット（Markdown）
# 週刊ガジェットレポート {week}

## 今週のサマリー

## 今週の注目新製品
（各製品について：スペック・価格・発売日・競合比較・おすすめ度を詳しく）

## GPU・CPU市場
### GPU動向
（RTX 5000シリーズ・Radeon RX 9000シリーズの最新情報・価格）
### CPU動向
（Ryzen 9000・Core Ultra 200の最新情報）
### 価格トレンド
（今週の価格変動・セール情報）

## PC・周辺機器
（注目のノートPC・デスクトップ・モニター・キーボード・マウス）

## スマートフォン・タブレット
（今週の発表・リーク・レビュー）

## 買い時・見送り判断まとめ
| カテゴリ | 判断 | 理由 |
|---|---|---|

## 来週の発表予定・注目イベント

## 情報源
""",

    "weekly_economics_en": f"""
You are an economic journalist for a premium financial publication. Create a comprehensive weekly economic intelligence report in English for the week of {week}.
Use web search to gather the latest information and write a detailed, substantive report.

## Target Topics
- Global macroeconomic trends and risks
- US Federal Reserve policy, inflation data, and labor market
- Bank of Japan policy, yen movements, and Japanese economy
- European Central Bank and EU economic dynamics
- China economic data and geopolitical risks
- Major market movements (equities, bonds, FX, commodities, crypto)
- Key economic data releases and their structural implications

## Target Reader
A Japanese IT engineer learning business English who is also a long-term index investor.
- TOEIC Reading 785, strong reading comprehension
- Use natural, professional English (The Economist / Financial Times / Bloomberg style)
- Sophisticated vocabulary and complex sentence structures are welcome — this is for language learning too
- Aim for depth over brevity: explain the "so what" behind every data point

## Writing Style
- Write like The Economist: confident, analytical, slightly opinionated but balanced
- Use active voice and precise economic terminology
- Each story should have: background → this week's development → market reaction → outlook
- Avoid bullet-point dumps; use well-constructed paragraphs

## Format (Markdown)
# Weekly Economic Intelligence {week}

## Executive Summary
(4-5 bullet points covering the week's most important developments)

## The Big Picture
(500-600 words: the overarching macro narrative tying together this week's events)

## Key Stories This Week
(4-5 stories, each 200-300 words, with context, market reaction, and 3-month outlook)

## Central Bank Watch
### Federal Reserve
### Bank of Japan
### European Central Bank

## Market Snapshot
| Asset | This Week | YTD | Key Driver |
|---|---|---|---|
(Include: S&P 500, Nikkei 225, USD/JPY, EUR/USD, 10Y UST, 10Y JGB, WTI Oil, Gold, BTC)

## Data Scorecard
(Key economic data released this week with actual vs. forecast vs. prior)

## Vocabulary & Phrases Corner
(5 key economic terms or phrases used this week, with definitions and example sentences)

## Next Week to Watch
(Calendar of key events with dates and expected market impact)

## Sources
""",
}


def generate_report(report_type: str) -> str:
    prompt = PROMPTS[report_type]

    if report_type in ("daily_economics_ja", "weekly_finance_ja"):
        market_snapshot = fetch_market_snapshot()
        prompt = f"""以下は本日取得した**実際の市場データ**です。レポート内の数値は必ずこのデータを使用してください。AIの学習データや推測で数値を補完することは絶対に禁止します。

{market_snapshot}

---

{prompt}"""

    response = client.responses.create(
        model="gpt-4o",
        tools=[{"type": "web_search_preview"}],
        input=prompt,
    )
    return response.output_text


def save_report(content: str, report_type: str) -> Path:
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path("reports") / report_type
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{date_str}.md"
    output_path.write_text(content, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("report_type", choices=list(PROMPTS.keys()))
    args = parser.parse_args()

    print(f"Generating: {args.report_type}")
    content = generate_report(args.report_type)
    path = save_report(content, args.report_type)
    print(f"Saved: {path}")
    print(content)
