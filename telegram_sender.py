import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("Token:", TELEGRAM_TOKEN)
print("Chat ID:", CHAT_ID)

def send_telegram_message(message):
    """
    Sends a Telegram message. If it exceeds 4096 characters, splits it into parts.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(f"[{timestamp}] ❌ Token or Chat ID not defined.")
        return

    max_length = 4000
    messages = [message[i:i+max_length] for i in range(0, len(message), max_length)]

    for i, part in enumerate(messages):
        data = {
            "chat_id": CHAT_ID,
            "text": part,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"[{timestamp}] ✅ Part {i+1}/{len(messages)} sent via Telegram.")
            else:
                print(f"[{timestamp}] ❌ Error sending part {i+1}. Code {response.status_code}")
                print("Response:", response.text)
        except Exception as e:
            print(f"[{timestamp}] ⚠️ Exception sending part {i+1} via Telegram: {e}")
