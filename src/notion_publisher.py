import os
import requests
from datetime import datetime

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DB_ID = os.environ.get("NOTION_DB_ID", "31a9b8c6-7a7f-8048-b072-df7114254a4f")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

REPORT_META = {
    "daily_economics_ja":  {"category": "ビジネス", "tags": ["ビジネス"]},
    "weekly_finance_ja":   {"category": "ビジネス", "tags": ["ビジネス", "重要"]},
    "weekly_servicenow_ja":{"category": "ServiceNow", "tags": ["技術"]},
    "weekly_career_ja":    {"category": "その他", "tags": ["個人メモ"]},
    "weekly_gadget_ja":    {"category": "その他", "tags": ["個人メモ"]},
    "weekly_economics_en": {"category": "ビジネス", "tags": ["ビジネス", "技術"]},
}


def create_page(title: str, report_type: str) -> str:
    meta = REPORT_META.get(report_type, {"category": "その他", "tags": []})
    today = datetime.now().strftime("%Y-%m-%d")

    payload = {
        "parent": {"database_id": NOTION_DB_ID},
        "properties": {
            "タイトル": {"title": [{"text": {"content": title}}]},
            "カテゴリー": {"select": {"name": meta["category"]}},
            "タグ": {"multi_select": [{"name": t} for t in meta["tags"]]},
            "ステータス": {"status": {"name": "公開済み"}},
            "作成日": {"date": {"start": today}},
        },
    }

    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    res.raise_for_status()
    return res.json()["id"]


def update_page_content(page_id: str, markdown: str) -> None:
    payload = {
        "page_id": page_id,
        "type": "replace_content",
        "replace_content": {"new_str": markdown},
    }
    res = requests.patch(
        f"https://api.notion.com/v1/pages/{page_id}/markdown",
        headers=HEADERS,
        json=payload,
    )
    res.raise_for_status()


def publish(title: str, content: str, report_type: str) -> str:
    page_id = create_page(title, report_type)
    update_page_content(page_id, content)
    return f"https://www.notion.so/{page_id.replace('-', '')}"
