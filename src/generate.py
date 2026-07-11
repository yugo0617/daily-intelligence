import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

today = datetime.now().strftime("%Y年%m月%d日")
week = datetime.now().strftime("%Y-W%W")

PROMPTS = {
    "daily_economics_ja": f"""
あなたは経済ジャーナリストです。{today}時点の経済朝刊を日本語で作成してください。

## 対象テーマ
- 日本経済（日銀・物価・賃金・財政・円相場）
- 世界経済（FRB・米国・中国・欧州）
- 市場（日経平均・S&P500・金利・為替・原油・金）

## 作成条件
- 過去24時間の重要ニュースを調査する
- 事実と解釈を明確に分ける
- 「何が起きたか」「なぜ起きたか」「今後何に影響するか」の順で説明する
- 株価変動の羅列ではなく、金融政策・物価・為替の因果関係を中心にする
- 日本在住のITエンジニア（長期インデックス投資家）への影響も簡潔に記載する
- 情報源と日付を付ける
- 5分で読める長さにする

## 出力フォーマット（Markdown）
# 経済朝刊 {today}

## 30秒要約
- （最重要ニュース1行）
- （市場全体の方向1行）
- （今日注目の指標1行）

## 本日の主要テーマ
（重要度順に2〜3件、各件について原因→市場反応→今後の注目点を説明）

## 市場概況
| 指標 | 動向 | 主な理由 |
|---|---|---|

## 今日の予定
（本日発表予定の経済指標・イベント）

## 情報源
""",

    "weekly_finance_ja": f"""
あなたは金融アナリストです。直近1週間（{week}）の金融市場・金融政策レポートを日本語で作成してください。

## 対象テーマ
- 日銀の金融政策・発言
- FRB・ECBの動向
- 日本の金融規制・FISC関連動向
- 株式・債券・為替市場の週次サマリー
- 仮想通貨の主要動向

## 作成条件
- ニュースの羅列ではなく因果関係で説明する
- 長期投資家の視点を含める
- 来週の重要イベント・指標を記載する

## 出力フォーマット（Markdown）
# 週刊金融レポート {week}

## 今週のサマリー（3行）

## 金融政策
## 市場動向
## 来週の注目イベント
## 情報源
""",

    "weekly_servicenow_ja": f"""
あなたはITアナリストです。直近1週間（{week}）のServiceNow・IT・AI業界の動向レポートを日本語で作成してください。

## 対象テーマ
- ServiceNowの新機能・リリース・コミュニティ動向
- AI・生成AIの最新動向（ビジネス活用・規制含む）
- クラウド・SaaSの主要ニュース
- サイバーセキュリティの重要インシデント

## 作成条件
- ServiceNow CSM/ITSM/CMDBエンジニアの視点で重要度を判断する
- 認定資格・試験に関連する情報があれば記載する
- 実務に使える情報を優先する

## 出力フォーマット（Markdown）
# 週刊IT・ServiceNowレポート {week}

## 今週のサマリー（3行）

## ServiceNow最新情報
## AI・生成AI動向
## セキュリティ
## 来週の注目
## 情報源
""",

    "weekly_career_ja": f"""
あなたはITキャリアアドバイザーです。直近1週間（{week}）のITエンジニア転職市場・年収動向レポートを日本語で作成してください。

## 対象テーマ
- ITエンジニアの求人動向・需要が高いスキル
- ServiceNow・クラウド・AI関連の年収相場
- 大手IT企業の採用動向
- エンジニアのキャリアに影響する業界ニュース

## ターゲット読者
2年目のServiceNowエンジニア（CSM/CMDB専門）。年収1000万円を目標としている。

## 出力フォーマット（Markdown）
# 週刊キャリア市場レポート {week}

## 今週のサマリー（3行）

## 需要が高いスキル・資格
## 年収・求人動向
## 今週の注目求人傾向
## 来週の注目
## 情報源
""",

    "weekly_gadget_ja": f"""
あなたはガジェットライターです。直近1週間（{week}）の新製品・テクノロジーガジェット動向レポートを日本語で作成してください。

## 対象テーマ
- PC・ノートPC・周辺機器の新製品・発表
- スマートフォン・タブレットの新情報
- GPU・CPU・メモリの価格動向
- ゲーミングデバイスの新製品
- コスパが良い注目製品

## 作成条件
- スペックと価格の両方を記載する
- 「買い時か」の判断基準も含める

## 出力フォーマット（Markdown）
# 週刊ガジェットレポート {week}

## 今週のサマリー（3行）

## 注目新製品
## 価格動向
## 買い時・見送り判断
## 来週の発表予定
## 情報源
""",

    "weekly_economics_en": f"""
You are an economic journalist. Create a weekly economic intelligence report in English for the week of {week}.

## Target Topics
- Global macroeconomic trends
- US Federal Reserve policy and decisions
- Bank of Japan policy and yen movements
- Major market movements (equities, bonds, FX, commodities)
- Key economic data releases and their implications

## Target Reader
A Japanese IT engineer learning business English.
- TOEIC Reading 785, strong reading comprehension
- Use natural, professional English (The Economist / Financial Times style)
- Avoid overly casual language; this is for language learning too

## Format (Markdown)
# Weekly Economic Intelligence {week}

## Executive Summary (3 bullet points)

## Key Stories This Week
(2-3 stories with context, market reaction, and outlook)

## Market Snapshot
| Asset | Movement | Key Driver |
|---|---|---|

## Vocabulary Corner
(3 key economic terms used this week, with definitions)

## Next Week to Watch

## Sources
""",
}


def generate_report(report_type: str) -> str:
    prompt = PROMPTS[report_type]
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
