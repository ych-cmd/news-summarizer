import feedparser
import time
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timedelta, timezone
from typing import List, Dict

RSS_URLS = [
    "https://news.google.com/rss/search?q=教育+OR+文部科学省+OR+中央教育審議会&hl=ja&gl=JP&ceid=JP:ja",
    "https://news.google.com/rss/search?q=大阪府教育委員会+OR+大阪市教育委員会+OR+すくすくウォッチ&hl=ja&gl=JP&ceid=JP:ja",
    "https://www.mext.go.jp/b_menu/news/index.rdf",
]

def _parse_entry(entry) -> Dict:
    """Convert a feedparser entry to a dict with needed fields."""
    title = entry.get("title", "(無題)")
    link = entry.get("link", "")
    # Some feeds provide 'published' or 'updated'
    published_str = entry.get("published", entry.get("updated", ""))
    # Parse date with feedparser's built‑in struct_time if possible
    published = None
    if "published_parsed" in entry and entry.published_parsed:
        # Convert struct_time to datetime in UTC
        published = datetime.fromtimestamp(
            time.mktime(entry.published_parsed), tz=timezone.utc
        )
    elif published_str:
        try:
            published = datetime.fromisoformat(published_str)
        except Exception:
            published = None
    # Fallback to now if parsing fails
    if not published:
        published = datetime.now(timezone.utc)
    # Some feeds have a summary / description
    summary = entry.get("summary", "")
    return {"title": title, "link": link, "published": published, "summary": summary}

def fetch_recent_articles(limit: int = 5) -> List[Dict]:
    """Fetch articles published in the last 24 hours from all RSS URLs.
    Returns a list of up to *limit* unique articles sorted by newest first.
    """
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=1)
    articles: List[Dict] = []
    seen_urls = set()
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            article = _parse_entry(entry)
            if article["link"] in seen_urls:
                continue
            if article["published"] < cutoff:
                continue
            seen_urls.add(article["link"])
            articles.append(article)
    # Sort by published descending and cut to limit
    articles.sort(key=lambda x: x["published"], reverse=True)
    return articles[:limit]

if __name__ == "__main__":
    for a in fetch_recent_articles():
        print(a["title"], a["link"], a["published"].isoformat())
