import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simple_moving_average(data,days):
    res = data['Adj Close'].rolling(window=days).mean()
    return res

def exponential_moving_average(data,days):
    res = data['Adj Close'].ewm(span=days,adjust=False).mean()
    return res

'''
Price crosses above 20-day SMA - buy
Price crosses below 20-day SMA - sell
Moving Average uses prior 19 days and current day - indicator is for next day
params: data = dataframe of historical data, current_day = day to get price for, window = days to compute MA
returns: 1 = buy else 0
'''
def sma_cross(data,window=20):
    curr_price = data['Adj Close'].iloc[-1]
    average = data['Adj Close'].iloc[-window:].mean()
    
    if curr_price > average:
        return 1
    else:
        return 0

'''
Uses two averages of different window sizes
100 day MA (Slow)- takes longer to adjust to sudden price changes
20 day MA (Fast)- faster to account for sudden changes
Fast MA crosses above slow MA - buy
Slow MA crosses above fast MA - sell
params: data = dataframe of historical data, current_day = day to get price for, fast_window = days to compute fast MA, slow_window = days to compute slow MA
returns: 1 = buy, else 0
'''
def moving_average_cross(data,fast_window=20,slow_window=100):
    slow_ma = round(data['Adj Close'].iloc[-slow_window:].mean(),2)
    fast_ma = round(data['Adj Close'].iloc[-fast_window:].mean(),2)
    
    if fast_ma > slow_ma:
        return 1
    else:
        return 0


'''
Moving Average Convergence/Divergence (MACD)
- indicator/oscillator for technical analysis
Composition
- MACD Series: difference between the fast and slow exponential moving averages (EMA)
- Signal: EMA on the MACD series
- Divergence: difference between MACD series and signal series
Logic
- MACD crosses above signal line -> buy
- MACD crosses below signal line -> sell
Returns: BUY signal if MACD line crosses above signal line and SELL signal if crosses below
'''
def moving_average_cd(data,slow_ema=26,fast_ema=12):
    data = data['Adj Close']
    
    slow = data.ewm(span=slow_ema,adjust=False).mean()
    fast = data.ewm(span=fast_ema,adjust=False).mean()

    macd = fast-slow
    signal = macd.ewm(span=9,adjust=False).mean()
    macd = macd.reset_index()
    signal = signal.reset_index()
    
    data = data.reset_index()
    data['MACD'] = macd['Adj Close']
    data['Signal'] = signal['Adj Close']
    
    if data['MACD'].iloc[-1] > data['Signal'].iloc[-1]:
        return 1
    else:
        return 0
    

'''
Relative Strength Index (RSI): Momentum oscillator that measures velocity and magnitude of directional price movements
- RSI crosses lower threshold -> buy
- RSI crosses upper threshold -> sell
returns: original dataframe with RSI column
'''
def relative_strength_index(data,lower_thresh=30,upper_thresh=70,period=14):
    data = data['Adj Close']
    data = data.iloc[-period:]
    difference = data.diff()
    
    gain,loss = difference.copy(),difference.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    
    gain_ema = gain.ewm(span=period-1,adjust=False).mean()
    loss_ema = loss.ewm(span=period-1,adjust=False).mean().abs()
    
    rs = gain_ema/loss_ema
    rsi = 100-(100/(1+rs))
    rsi = rsi.reset_index()
    data = data.reset_index()
    data['RSI'] = rsi['Adj Close']
    
    if data['RSI'].iloc[-1] > lower_thresh:
        return 1
    elif data['RSI'].iloc[-1] > upper_thresh:
        return -1
    else:
        return 0

'''
Money Flow Index (MFI): technical oscillator that uses price and volume data for identifying overbought/oversold signals
- MFI > 80 = overbought and MFI < 20 = oversold
Formulas
- Money Flow Index (MFI) = 100 - (100/(1 + MFR))
- Money Flow Ratio (MFR) = Sum of 14 day positive flow / Sum of 14 day negative flow
- Typical Price (TP) = (high + low + close) / 3
- Raw Money Flow (RMF) = TP * Volume
'''
def money_flow_index(data):
    mfi = 0
    df = data.tail(15)
    
    # calculate typical price of last 14 days
    df['Typical Price'] = (df['High'] + df['Low'] + df['Close'])/3
    df = df.round(2)
    df['Temp'] = df['Typical Price'].shift(1)
    df.dropna(inplace=True)
    df['RMF Sign'] = df['Typical Price'] >= df['Temp']
    df.drop('Temp',axis=1,inplace=True)

    # calculate RMF
    df['RMF'] = df['Typical Price'] * df['Volume']
    for row in list(df.index):
        if not df.loc[row,'RMF Sign']:
            df.loc[row,'RMF'] *= -1

    # calculate MFR
    pos,neg = 0,0
    mfr = 0
    for val in df['RMF'].values:
        if val >= 0:
            pos += val
        else:
            neg += val*-1
    #print(pos,neg)
    mfr = pos/neg

    # money flow index
    mfi = 100 - (100/(1 + mfr))
    return round(mfi,2)
