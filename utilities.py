import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simple_moving_average(data,days):
    res = data['Adj Close'].rolling(window=days).mean()
    return round(res.iloc[-1],2)

def exponential_moving_average(data,days):
    res = data['Adj Close'].ewm(span=days,adjust=False).mean()
    return res#round(res.iloc[-1],2)

def moving_avg_cross(data,days_short,days_long):
    short_avg = simple_moving_average(data,days_short)
    long_avg = simple_moving_average(data,days_long)
    
    return short_avg > long_avg
    
'''
Buy if 30 day MA crosses below 90 day MA
'''
def mean_reversion(data):
    thirty_day_ma = simple_moving_average(data,30)
    ninety_day_ma = simple_moving_average(data,90)
    return thirty_day_ma < ninety_day_ma

'''
Buy if stock is at a 20 day high
'''
def turtle(data):
    curr_price = data['Adj Close'].iloc[-1]
    prev_prices = list(data['Adj Close'].iloc[-21:-1])
    highest = max(prev_prices)
    return curr_price > highest


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
    
    rsi = data['RSI'].iloc[-1]
    return rsi
    

'''
Money Flow Index (MFI): technical oscillator that uses price and volume data for identifying overbought/oversold signals
- MFI > 70 = overbought and MFI < 30 = oversold
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
    
    return mfi
       