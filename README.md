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

algo-trading-ensemble-ml-bot/
│
├── 📄 .env                         → Environment variables (API keys, Telegram tokens)
├── 📄 .gitignore                   → Ignore credentials, cache, etc. in Git
├── ⚙️ config.py                    → Central config: stock list, sheet names, paths
├── 🔒 credentials.json             → Google Service Account credentials (⚠️ do NOT upload)
├── 🚀 main.py                      → Main script: fetch data → backtest → ML → log → notify
├── 📝 README.md                    → Project overview and documentation
├── 📦 requirements.txt             → Python dependencies (yfinance, XGBoost, gspread, etc.)
│
├── 📁 .github/
│   └── 🔄 workflows/
│       └── main.yml               → Optional GitHub Actions automation (CI/CD)
│
├── 📁 utils/                       → Core logic organized by role
│   ├── 📊 backtester.py           → Simulates trading and calculates performance
│   ├── 🔍 data_fetcher.py         → Pulls stock data from Yahoo Finance (yfinance)
│   ├── 📋 google_sheets.py        → Logs trades & applies formatting in Google Sheets
│   ├── 📈 indicators.py           → Calculates RSI, moving averages, MACD, etc.
│   ├── 🤖 ml_model.py             → Stacking ML model (LR + RF + XGBoost)
│   ├── 📣 notifier.py             → Sends trade alerts via Telegram bot
│   ├── 🧠 strategy.py             → Encapsulates RSI + DMA crossover strategy
│   └── 🧪 tempCodeRunnerFile.py   → Temporary script (can be ignored or removed)
│
└── 📁 __pycache__/                → Auto-generated Python bytecode (ignored in Git)



🛠️ Developed By
Built with 💻 by Krunal Wankhade
📬 Connect on LinkedIn
🚀 Passionate about AI, trading systems, and clean, scalable code.