"""yfinanceで実際の市場データを取得する"""
import yfinance as yf
from datetime import datetime, timedelta


TICKERS = {
    "日経平均":    "^N225",
    "TOPIX":       "^TPX",
    "S&P500":      "^GSPC",
    "ナスダック":  "^IXIC",
    "ドル円":      "USDJPY=X",
    "ユーロ円":    "EURJPY=X",
    "米10年債利回り": "^TNX",
    "日10年債利回り": "^JGB10Y",
    "WTI原油":     "CL=F",
    "金":          "GC=F",
    "BTC/USD":     "BTC-USD",
}


def fetch_market_snapshot() -> str:
    lines = [f"## 実市場データ（{datetime.now().strftime('%Y-%m-%d %H:%M')} JST取得）\n"]
    lines.append("| 指標 | 現値 | 前日比 | 前日比% |")
    lines.append("|---|---|---|---|")

    for name, ticker in TICKERS.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) < 2:
                hist = t.history(period="5d")
            if len(hist) >= 2:
                prev = hist["Close"].iloc[-2]
                curr = hist["Close"].iloc[-1]
                diff = curr - prev
                pct = diff / prev * 100
                sign = "+" if diff >= 0 else ""
                lines.append(f"| {name} | {curr:,.2f} | {sign}{diff:,.2f} | {sign}{pct:.2f}% |")
            elif len(hist) == 1:
                curr = hist["Close"].iloc[-1]
                lines.append(f"| {name} | {curr:,.2f} | N/A | N/A |")
            else:
                lines.append(f"| {name} | データ取得失敗 | - | - |")
        except Exception as e:
            lines.append(f"| {name} | エラー: {e} | - | - |")

    return "\n".join(lines)


if __name__ == "__main__":
    print(fetch_market_snapshot())
