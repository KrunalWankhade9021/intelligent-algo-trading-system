import yfinance as yf

def fetch_data(ticker, period="12mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data