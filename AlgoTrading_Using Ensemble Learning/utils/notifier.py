import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(message, retries=3, delay=3):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    for attempt in range(1, retries + 1):
        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            print(f"📤 Telegram message sent successfully.")
            return
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Telegram attempt {attempt} failed: {e}")
            if attempt < retries:
                print(f"🔁 Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("❌ All retries failed. Telegram message not sent.")
