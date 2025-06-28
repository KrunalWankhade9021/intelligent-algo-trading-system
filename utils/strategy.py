from utils.indicators import calculate_rsi, add_moving_averages

def generate_signals(data):
    data = calculate_rsi(add_moving_averages(data))
    data['Signal'] = 0
    data.loc[(data['RSI'] < 40) & (data['20DMA'] > data['50DMA']), 'Signal'] = 1
    return data
