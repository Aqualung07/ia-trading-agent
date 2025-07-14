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
    Envía un mensaje por Telegram. Si supera los 4096 caracteres, lo divide en partes.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(f"[{timestamp}] ❌ Token o Chat ID no definidos.")
        return

    max_length = 4000
    messages = [message[i:i+max_length] for i in range(0, len(message), max_length)]

    for i, part in enumerate(messages):
        data = {
            "chat_id": CHAT_ID,
            "text": part,
            # "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print(f"[{timestamp}] ✅ Parte {i+1}/{len(messages)} enviada por Telegram.")
            else:
                print(f"[{timestamp}] ❌ Error al enviar parte {i+1}. Código {response.status_code}")
                print("Respuesta:", response.text)
        except Exception as e:
            print(f"[{timestamp}] ⚠️ Excepción al enviar parte {i+1} por Telegram: {e}")
