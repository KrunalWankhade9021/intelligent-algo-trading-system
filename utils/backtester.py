from utils.strategy import generate_signals

def backtest(data):
    data = generate_signals(data)
    data['Position'] = data['Signal'].shift(1).fillna(0)
    data['Returns'] = data['Close'].pct_change()
    data['Strategy'] = data['Returns'] * data['Position']

    total_return = (data['Strategy'] + 1).prod() - 1
    win_ratio = (data['Strategy'] > 0).sum() / (data['Strategy'] != 0).sum()
    return total_return, win_ratio, data
