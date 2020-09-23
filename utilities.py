import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

################# DESCRIPTORS #################
'''
Computes which direction a stock is currently trending 
'''
def trend_direction(data,date):
    df = data.copy()
    df = df[['Adj Close','High','Low']].round(2)
    df['date_id'] = ((df.index.date - df.index.date.min())).astype('timedelta64[D]')
    df['date_id'] = df['date_id'].dt.days + 1
    
    df = df.loc[:date,:]
    start = (df['date_id'].iloc[-5],df['Adj Close'].iloc[-5])
    end = (df['date_id'].iloc[-1],df['Adj Close'].iloc[-1])
    
    slope = round((end[1] - start[1]) / (end[0]-start[0]),2)
    if slope > 0:
        return 'UP'
    if slope <= 0:
        return 'DOWN'


################# INDICATORS #################
'''
Calaculates simple moving average over the specified
'''
def simple_moving_average(data,days,end_date):
    days = int(days)
    df = data.copy()
    df = df.loc[:end_date,:]
    avg = df['Adj Close'].rolling(days).mean()
    return round(avg.iloc[-1],2)

'''
Relative Strength Index (RSI): Momentum oscillator that measures velocity and magnitude of directional price movements
- RSI crosses lower threshold -> buy
- RSI crosses upper threshold -> sell
returns: original dataframe with RSI column
'''
def relative_strength_index(data,period=14):
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
    return round(rsi,2)

'''
Bollinger Bands
- Volatility indicator
- Comprises of 2 lines plotted 2 standard deviations from a m (around 20) period simple moving avg line
- Bands widen during increased volatility and shrink during decreased
- overbought if price is closer to upper band, oversold if price is closer to lower band
'''
def bollinger_bands(data,n=20):
    df = data.copy()
    df['SMA'] = df['Adj Close'].rolling(n).mean()
    df['UPPER'] = df['SMA'] + 2*df['SMA'].rolling(n).std()
    df['LOWER'] = df['SMA'] - 2*df['SMA'].rolling(n).std()
    df['WIDTH'] = df['UPPER'] - df['LOWER']
    df.dropna(inplace=True)
    df = df.round(2)
    df = df[['Adj Close','UPPER','LOWER','WIDTH']]
    return df
