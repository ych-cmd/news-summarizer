import os
from dotenv import load_dotenv

load_dotenv()   # カレントディレクトリの .env を読み込む

key = os.getenv('GEMINI_API_KEY')
if key:
    print('GEMINI_API_KEY:', key[:10] + '...')
else:
    print('GEMINI_API_KEY: 未設定')
