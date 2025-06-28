from utils.data_fetcher import fetch_data
from utils.google_sheets import connect_to_sheets, log_trade, apply_conditional_formatting
from utils.backtester import backtest
from utils.ml_model import train_model
from utils.notifier import send_telegram  # Telegram notification active
from config import API_STOCKS
from datetime import datetime
import schedule
import time
import os
import base64

# 🔓 Decode credentials.json if running from an environment variable
if os.getenv("ENCODED_GOOGLE_CREDS"):
    with open("credentials.json", "wb") as f:
        f.write(base64.b64decode(os.getenv("ENCODED_GOOGLE_CREDS")))

def run_trading_job():
    sheet = connect_to_sheets()

    for stock in API_STOCKS:
        print(f"\n📱 Fetching data for {stock}...")
        df = fetch_data(stock)

        if df is None or df.empty:
            print(f"❌ Skipping {stock} - no data received.")
            continue

        try:
            total_return, win_ratio, result_df = backtest(df)
        except Exception as e:
            print(f"⚠️ Backtesting failed for {stock}: {e}")
            continue

        if result_df is None or result_df.empty:
            print(f"⚠️ No trades/backtest results for {stock}. Skipping ML & logging.")
            continue

        try:
            model, accuracy = train_model(result_df)
            model_type = type(model).__name__
        except Exception as e:
            print(f"⚠️ ML training failed for {stock}: {e}")
            accuracy = None
            model_type = "N/A"

        accuracy_str = f"{accuracy:.2%}" if accuracy is not None else "N/A"

        try:
            log_trade(sheet, [
                stock,
                f"{total_return:.2%}",
                f"{win_ratio:.2%}",
                accuracy_str
            ])
        except Exception as e:
            print(f"⚠️ Failed to log {stock} to Google Sheets: {e}")
            continue

        print(f"✅ Logged: {stock} | Return: {total_return:.2%}, Win Ratio: {win_ratio:.2%}, "
              f"ML Accuracy: {accuracy_str} | Model: {model_type}")

        try:
            message = f'''
📈 Algo-Trading Signal ({datetime.now().strftime('%d %B %Y')})

🔹 Stock: {stock}
🔸 Strategy: RSI < 40 + 20DMA > 50DMA
🔹 Backtest Return: {total_return:.2%}
🔹 Win Ratio: {win_ratio:.2%}
🔹 ML Accuracy: {accuracy_str}
🔹 Model Used: {model_type}
'''
            send_telegram(message.strip())
        except Exception as e:
            print(f"⚠️ Telegram message failed: {e}")

    try:
        apply_conditional_formatting()
    except Exception as e:
        print(f"⚠️ Failed to apply conditional formatting: {e}")

# 🔁 Run job once manually
run_trading_job()

# Optional: Schedule to run daily
# schedule.every().day.at("09:15").do(run_trading_job)
# while True:
#     schedule.run_pending()
#     time.sleep(60)
