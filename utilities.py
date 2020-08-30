import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    df['DIFF UPPER'] = df['Adj Close'] - df['UPPER']
    df['DIFF LOWER'] = df['Adj Close'] - df['LOWER']
    df = df.abs()

    df['TEMP'] = df['DIFF UPPER'] > df['DIFF LOWER']
    df.loc[df['TEMP'] == True,'SIGNAL'] = 1
    df.loc[df['TEMP'] == False,'SIGNAL'] = -1
    df.drop('TEMP',axis=1,inplace=True)
    return df.iloc[-1]

'''
Average True Range
- Volatility indicator
- Accounts the market movement each day in either direction & averaging them out
- Focuses on total price movement and conveys how widly the market is swinging as it moves
'''
def average_true_range(data,n=20):
    df = data.copy()
    df['HIGH-LOW'] = abs(df['High']-df['Low'])
    df['HIGH-PREV CLOSE'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['LOW-PREV CLOSE'] = abs(df['Low'] - df['Adj Close'].shift(1))
    
    df['TRUE RANGE'] = df[['HIGH-LOW','HIGH-PREV CLOSE','LOW-PREV CLOSE']].max(axis=1,skipna=False)
    df['AVERAGE TRUE RANGE'] = df['TRUE RANGE'].rolling(n).mean()
    df = df[['TRUE RANGE','AVERAGE TRUE RANGE']]
    df = df.round(2)
    df.dropna(inplace=True)
    return df['AVERAGE TRUE RANGE'].iloc[-1]

'''
Average Directional Index
 - Way to measure the strength of a trend
 - Vals range 0-100 where 100 is very strong and 0 is weak
 - Non directional, only focuses on the strength of a trend not the direction
'''

'''
On Balance Volume
- Momentum indicator which uses changes in volume to indicate future price movements
- Rising obv reflects positive volume pressure that can lead to higher prices, falling predicts price declines
'''