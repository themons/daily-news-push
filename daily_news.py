import requests
import json
import os
import re
from datetime import datetime

PUSHPLUS_TOKEN = os.environ["PUSHPLUS_TOKEN"]

NEWS_SOURCES = {
    "国家大事": [
        "site:gov.cn OR site:xinhuanet.com OR site:people.com.cn 最新政策",
        "中国国务院 最新消息",
    ],
    "今日要闻": [
        "中国今日新闻 头条",
        "今日热点新闻",
    ],
    "民生趣闻": [
        "民生新闻 有趣",
        "生活趣闻 社会",
    ],
}


def search_news(query):
    """通过 DuckDuckGo 获取新闻"""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get("https://html.duckduckgo.com/html/", params={"q": query}, headers=headers, timeout=15)
        results = []
        for m in re.findall(r'<a rel="nofollow" class="result__a" href="[^"]+">(.*?)</a>', resp.text):
            text = re.sub(r'<[^>]+>', '', m).strip()
            if len(text) > 10 and len(text) < 100:
                results.append(text)
        return results
    except Exception:
        return []


def search_history_today():
    """历史上的今天"""
    month, day = datetime.now().month, datetime.now().day
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(
            f"https://zh.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}",
            headers=headers, timeout=15
        )
        data = resp.json()
        events = []
        for item in data.get("events", [])[:10]:
            year = item.get("year", "")
            text = item.get("text", "")
            if text:
                events.append(f"{year}年 — {text[:60]}")
        return events
    except Exception:
        return []


def search_personnel():
    """人事变动"""
    try:
        return search_news("人事任免 任命 调整 最新")
    except Exception:
        return []


def build_news():
    news = {}
    total = 0

    # 国家大事
    items = search_news("中国 最新政策 国家大事 2025")
    news["🏛️ 国家大事"] = items[:4]
    total += len(news["🏛️ 国家大事"])

    # 今日要闻
    items = search_news("今日要闻 热点新闻 头条")
    news["📰 今日要闻"] = items[:4]
    total += len(news["📰 今日要闻"])

    # 民生趣闻
    items = search_news("民生趣闻 暖心 社会新闻")
    news["😊 民生趣闻"] = items[:4]
    total += len(news["😊 民生趣闻"])

    # 古今今日
    history = search_history_today()
    news["📜 古今今日"] = history[:3]
    total += len(news["📜 古今今日"])

    # 今日人事
    personnel = search_personnel()
    news["🌅 今日人事"] = personnel[:3]
    total += len(news["🌅 今日人事"])

    return news, total


def format_news(news):
    today = datetime.now().strftime("%Y年%m月%d日")
    lines = [f"📰 每日早报 | {today}\n"]
    lines.append("━" * 24)

    for category, items in news.items():
        lines.append(f"\n{category}")
        if not items:
            lines.append("  暂无相关新闻")
        for i, item in enumerate(items, 1):
            lines.append(f"  {i}. {item}")

    lines.append("\n" + "━" * 24)
    lines.append("☀️ 新的一天，加油！")

    return "\n".join(lines)


def send_pushplus(content):
    url = f"http://www.pushplus.plus/send"
    payload = {
        "token": PUSHPLUS_TOKEN,
        "title": f"📰 每日早报 | {datetime.now().strftime('%m月%d日')}",
        "content": content.replace("\n", "<br>"),
        "template": "html",
    }
    resp = requests.post(url, json=payload, timeout=15)
    result = resp.json()
    if result.get("code") == 200:
        print("✅ 推送成功！")
    else:
        print(f"❌ 推送失败: {result}")


if __name__ == "__main__":
    print("🔍 正在搜索新闻...")
    news, total = build_news()
    print(f"📋 共获取 {total} 条新闻")
    content = format_news(news)
    print(content)
    print("\n📤 正在推送到微信...")
    send_pushplus(content)
