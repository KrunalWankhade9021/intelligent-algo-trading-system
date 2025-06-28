# 📈 Algo-Trading System with ML & Automation

This project is a Python-based algorithmic trading bot that:
- Fetches stock data from Yahoo Finance
- Applies a simple trading strategy (RSI < 40 + 20DMA > 50DMA)
- Logs trades to Google Sheets
- Sends alerts via Telegram
- Automatically runs every day using GitHub Actions

---

## 🚀 Features

- 🔁 **Daily Automation** using GitHub Actions (runs at 9:15 AM IST)
- 📊 **Trading Strategy**:
  - Buy signal if RSI < 40
  - Confirmed when 20-day Moving Average crosses above 50-day MA
- 🔙 **6-Month Backtesting**
- 📈 **P&L and Win Ratio Logging** in Google Sheets
- 🤖 **ML Bonus**: Optional Logistic Regression model to predict next-day movement
- 📩 **Telegram Alerts** for daily trade signals

---

## 🧰 Technologies Used

- Python
- `yfinance`, `pandas`, `ta`, `scikit-learn`
- Google Sheets API
- Telegram Bot API
- GitHub Actions (Free CI/CD automation)

---

## 📂 Project Structure
```bash
.
├── main.py                 # Main execution script
├── config.py               # Google Sheets + Telegram config
├── requirements.txt        # All required Python packages
├── .github/workflows/
│   └── main.yml            # GitHub Actions workflow (runs daily)
├── utils/
│   └── strategy.py         # Strategy logic and indicators
├── data/                   # Saved data (optional)
├── logs/                   # Logs trades & messages (optional)
├── README.md               # You are here
└── .gitignore              # Excludes sensitive files
```
## 🔐 GitHub Secrets (Required)

Secret Name	Description
ENCODED_GOOGLE_CREDS	Base64 string of credentials.json
TELEGRAM_BOT_TOKEN	Your bot’s token from BotFather
TELEGRAM_CHAT_ID	Your chat ID from /getUpdates API

## 🛠️ Setup Instructions (For Local Use)

git clone https://github.com/ArpitChb2704/algo-trading-system.git
cd algo-trading-system

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

python main.py

