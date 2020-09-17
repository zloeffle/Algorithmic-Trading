import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

################# DESCRIPTORS #################
def support_level(data,start,end):
    df = data.copy()
    df = df['Adj Close'].round(2)
    price = df.min()
    date = df.idxmin()
    print(price,date)
    return price,date

def resistance_level(data,start,end):
    df = data.copy()
    df = df['Adj Close'].round(2)
    price = df.max()
    date = df.idxmax()
    print(price,date)
    return price,date

def trend(data,start,end):
    df = data.copy()
    df = df[['Adj Close','High','Low']].round(2)
    df['date_id'] = ((df.index.date - df.index.date.min())).astype('timedelta64[D]')
    df['date_id'] = df['date_id'].dt.days + 1
    
    start = (df.loc[start,'date_id'],df.loc[start,'Adj Close'])
    end = (df.loc[end,'date_id'],df.loc[end,'Adj Close'])
    
    slope = round((end[1] - start[1]) / (end[0]-start[0]),2)
    
    if slope > 0:
        return 'UP'
    return 'DOWN'

def breakout(data,start,end,price):
    support = support_level(data,start,end)
    resistance = resistance_level(data,start,end)
    
    if price > support[0]:
        return 'UP'
    elif price < resistance[0]:
        return 'DOWN'
    else:
        return 'NONE'

################# INDICATORS #################

def simple_moving_average(data,days,end_date):
    df = data.copy()
    df = df.loc[:end_date,:]
    avg = df['Adj Close'].rolling(days).mean()
    return round(avg.iloc[-1],2)

def exponential_moving_average(data,days,end_date):
    df = data.copy()
    df = df.loc[:end_date,:]
    avg = df['Adj Close'].ewm(days).mean()
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
    #print(data)
    
    rsi = data['RSI'].iloc[-1]
    return round(rsi,2)

def rsi_signal(rsi,lower_thresh=30,upper_thresh=70):
    if rsi <= lower_thresh:
        return 1
    elif rsi >= upper_thresh:
        return -1
    else:
        return 0

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

def bollinger_bands_signal(data):
    df = data.copy()
    if not df.empty:
        df['DIFF UPPER'] = df['Adj Close'] - df['UPPER']
        df['DIFF LOWER'] = df['Adj Close'] - df['LOWER']
        df = df.abs()

        df['TEMP'] = df['DIFF UPPER'] > df['DIFF LOWER']
        df.loc[df['TEMP'] == True,'SIGNAL'] = 1
        df.loc[df['TEMP'] == False,'SIGNAL'] = -1
        df.drop('TEMP',axis=1,inplace=True)
        return df['SIGNAL'].iloc[-1]
    return 0