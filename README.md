# daily-intelligence

OpenAI のウェブ検索と yfinance の実市場データを組み合わせて、経済・金融・IT・キャリア・ガジェットのレポートを自動生成し、Markdown として保存しつつ Notion に自動投稿する仕組みです。GitHub Actions で毎日・毎週スケジュール実行されます。

## できること

- **毎日**: 経済朝刊（`daily_economics_ja`）を平日中心に自動生成
- **毎週**: 金融・ServiceNow/IT・キャリア市場・ガジェット・英語経済レポートの5種類をまとめて自動生成
- 日経平均・為替・米国債利回りなどの実市場データを yfinance で取得し、レポート内の数値がハルシネーションしないようプロンプトに埋め込み
- 生成したレポートを `src/reports/<report_type>/<日付>.md` として保存し、リポジトリにコミット
- `NOTION_TOKEN` が設定されていれば Notion データベースにも自動投稿

## レポート種別

| report_type | 内容 | 頻度 |
|---|---|---|
| `daily_economics_ja` | 経済朝刊（日本経済・世界経済・市場概況） | 毎日 |
| `weekly_finance_ja` | 週刊金融レポート（中央銀行・株式・債券・為替） | 週次 |
| `weekly_servicenow_ja` | 週刊IT・ServiceNowレポート | 週次 |
| `weekly_career_ja` | 週刊キャリア市場レポート（ITエンジニア転職・年収） | 週次 |
| `weekly_gadget_ja` | 週刊ガジェットレポート（PC・GPU・スマホ） | 週次 |
| `weekly_economics_en` | Weekly Economic Intelligence（英語） | 週次 |

## セットアップ

```bash
pip install -r requirements.txt
```

必要な環境変数:

| 変数名 | 必須 | 説明 |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | レポート生成（`gpt-4o` + web search）に使用 |
| `NOTION_TOKEN` | 任意 | 設定するとレポートを Notion に自動投稿 |
| `NOTION_DB_ID` | 任意 | 投稿先の Notion データベースID（未設定時はデフォルト値を使用） |

## 使い方

```bash
cd src
python run.py daily_economics_ja
```

`report_type` には上記テーブルのいずれかを指定します。生成 → `reports/<report_type>/<日付>.md` に保存 → `NOTION_TOKEN` があれば Notion 投稿、の順に処理されます。

市場データ単体の確認:

```bash
python src/market_data.py
```

## 自動実行（GitHub Actions）

- `.github/workflows/daily.yml`: 平日を中心に毎日 JST 7:30 頃に `daily_economics_ja` を生成・コミット
- `.github/workflows/weekly.yml`: 毎週日曜 JST 9:00 に週次レポート5種を並列生成・コミット

いずれも `workflow_dispatch` に対応しており、GitHub Actions の画面から手動実行も可能です。実行には リポジトリの Secrets に `OPENAI_API_KEY`（必須）、`NOTION_TOKEN` / `NOTION_DB_ID`（任意）の登録が必要です。

## ディレクトリ構成

```
src/
├── run.py              # エントリーポイント（生成→保存→Notion投稿）
├── generate.py         # レポート種別ごとのプロンプト定義とOpenAI呼び出し
├── market_data.py      # yfinanceによる実市場データ取得
├── notion_publisher.py # Notion API連携
└── reports/            # 生成されたレポート（report_type別ディレクトリ）
.github/workflows/
├── daily.yml           # 毎日の経済朝刊生成ワークフロー
└── weekly.yml          # 週次レポート生成ワークフロー
```
