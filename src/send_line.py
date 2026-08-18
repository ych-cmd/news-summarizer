import os
import json
from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_USER_ID:
    raise RuntimeError("LINE_CHANNEL_ACCESS_TOKEN or LINE_USER_ID not set in environment")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def push_message(text: str) -> dict:
    """Push a text message to the user.
    Returns the decoded JSON response from the API for logging.
    """
    message = TextSendMessage(text=text)
    response = line_bot_api.push_message(LINE_USER_ID, message)
    # line-bot-sdk returns a dict-like object; convert to json for consistency
    return json.loads(json.dumps(response, default=str))

if __name__ == "__main__":
    # simple manual test
    sample = "テストメッセージ: LINE 送信が成功しました。"
    print(push_message(sample))
