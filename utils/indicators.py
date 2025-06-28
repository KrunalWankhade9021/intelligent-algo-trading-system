def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi
    return data

def add_moving_averages(data):
    data['20DMA'] = data['Close'].rolling(window=20).mean()
    data['50DMA'] = data['Close'].rolling(window=50).mean()
    return data