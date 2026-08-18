import os
from datetime import datetime
from src.fetch_rss import fetch_recent_articles
from src.summarize import summarize_articles
from src.send_line import push_message
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def build_message(summary_text: str) -> str:
    """Add a date header if not already present and ensure correct line breaks.
    The Gemini output already includes the desired format, but we prepend the
    current date header as a safety net.
    """
    today = datetime.now().strftime('%Y/%m/%d')
    header = f"📅 【今朝の教育時事ダイジェスト】{today}\n"
    # If the Gemini output already starts with the header, avoid duplication
    if summary_text.lstrip().startswith('📅'):
        return summary_text
    return header + summary_text

def main():
    try:
        logging.info('Fetching recent articles...')
        articles = fetch_recent_articles()
        if not articles:
            logging.warning('No recent articles found in the last 24h.')
            fallback_msg = f"📅 【今朝の教育時事ダイジェスト】{datetime.now().strftime('%Y/%m/%d')}\n\n本日の教育ニュースは取得できませんでした。"
            push_message(fallback_msg)
            return
        logging.info(f'Fetched {len(articles)} articles.')
        logging.info('Generating summary with Gemini...')
        summary = summarize_articles(articles)
        message = build_message(summary)
        logging.info('Pushing message to LINE...')
        push_message(message)
        logging.info('Message sent successfully.')
    except Exception as e:
        logging.exception('Unexpected error occurred')
        error_msg = f"📅 【今朝の教育時事ダイジェスト】{datetime.now().strftime('%Y/%m/%d')}\n\nエラーが発生しました: {str(e)}"
        try:
            push_message(error_msg)
        except Exception:
            logging.exception('Failed to send error notification to LINE')

if __name__ == '__main__':
    main()
