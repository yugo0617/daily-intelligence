"""エントリーポイント: レポート生成 → 保存 → Notion投稿"""
import os
import sys
from datetime import datetime
from generate import generate_report, save_report, PROMPTS
from notion_publisher import publish


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python run.py <report_type>")
        print(f"Available: {', '.join(PROMPTS.keys())}")
        sys.exit(1)

    report_type = sys.argv[1]
    if report_type not in PROMPTS:
        print(f"Unknown report type: {report_type}")
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    titles = {
        "daily_economics_ja":  f"経済朝刊 {today}",
        "weekly_finance_ja":   f"週刊金融レポート {today}",
        "weekly_servicenow_ja":f"週刊IT・ServiceNowレポート {today}",
        "weekly_career_ja":    f"週刊キャリア市場レポート {today}",
        "weekly_gadget_ja":    f"週刊ガジェットレポート {today}",
        "weekly_economics_en": f"Weekly Economic Intelligence {today}",
    }

    print(f"[1/3] Generating {report_type}...")
    content = generate_report(report_type)

    print(f"[2/3] Saving to file...")
    path = save_report(content, report_type)
    print(f"      Saved: {path}")

    if os.environ.get("NOTION_TOKEN"):
        print(f"[3/3] Publishing to Notion...")
        url = publish(titles[report_type], content, report_type)
        print(f"      Published: {url}")
    else:
        print(f"[3/3] NOTION_TOKEN not set, skipping Notion publish")

    print("Done.")


if __name__ == "__main__":
    main()
