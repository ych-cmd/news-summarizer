import os
import json
from typing import List, Dict
import google.generativeai as genai
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Load API key from environment (only API key is used)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")
genai.configure(api_key=GEMINI_API_KEY)

# Use the latest public model
model = genai.GenerativeModel('gemini-3.6-flash')

SYSTEM_PROMPT = (
    "あなたは教育行政および学校経営の専門家（指導主事）です。"
    "まず全国的なニュースを中心に要約し、次に大阪府・支援学校に関する情報があれば、追加で重点的に評価してください。"
    "各記事について、事実の羅列ではなく教育現場や行政への影響・指導主事としての着眼点を含めて簡潔にまとめてください。"
)

def build_prompt(articles: List[Dict]) -> str:
    """Create the prompt for Gemini from a list of article dicts.
    Each dict contains: title, link, summary (optional), published.
    """
    lines = [SYSTEM_PROMPT, "以下の情報を元に要約を作成してください。\n"]
    for idx, a in enumerate(articles, 1):
        lines.append(f"## 記事{idx}\nタイトル: {a['title']}\nURL: {a['link']}\n概要: {a.get('summary', '')}\n公開日時: {a['published'].isoformat()}\n")
    lines.append(
        "出力は以下のフォーマットでお願いします：\n"
        "📅 【今朝の教育時事ダイジェスト】YYYY/MM/DD\n"
        "━━━━━━━━━━━━\n"
        "📰 [記事タイトル]\n"
        "🔗 [URL]\n"
        "・【概要】（何が決まった/起きたか：40〜60字）\n"
        "・【教育的論点・現場視点】（なぜ重要か/どう対応すべきか：60〜80字）\n"
        "━━━━━━━━━━━━\n"
        "（※3〜5記事分繰り返す）"
    )
    return "\n".join(lines)

def summarize_articles(articles: List[Dict]) -> str:
    prompt = build_prompt(articles)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # simple test with dummy data
    sample = [{
        "title": "サンプル記事",
        "link": "https://example.com",
        "summary": "これはサンプルです。",
        "published": datetime.now()
    }]
    print(summarize_articles(sample))
