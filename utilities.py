from operator import truediv
from matplotlib.pyplot import plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

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
Calculates slope between two data points
'''
def slope(y2,y1,x2,x1):
    return round((y2-y1)/(x2-x1),2)

'''
Computes which direction a stock is currently trending over a specified period
'''
def peaks_and_valleys(data,period=31,plot=False):
    df = data.copy()
    df = df[['Adj Close','High','Low']].round(2)
    df = df.iloc[-period:]
    df['date_id'] = range(1,len(df)+1)
   
    x = np.array(df['date_id'])
    y = np.array(df['Adj Close'])
    # plot data
    if plot:
        plt.plot(x,y)
        plt.xticks(np.arange(min(x),max(x)+1,1.0))
        plt.show()
        
    # set index as integer scale
    df.index = df['date_id']
    
    # Get peaks and valleys to compute trend direction
    peaks = []
    valleys = []
    for i in range(2,len(df),1):
        curr = df.loc[i,'Adj Close']
        lower = df.loc[i-1,'Adj Close']
        upper = df.loc[i+1,'Adj Close']
        
        # peaks
        if curr > lower and curr > upper:
            peaks.append(i)
        
        # valleys
        if curr < lower and curr < upper:
            valleys.append(i)
    
    peaks = df[df.index.isin(peaks)]
    valleys = df[df.index.isin(valleys)]
    valleys = valleys[valleys.index > peaks.index[0]]
    
    return peaks,valleys

def trend_direction(data):
    peaks,valleys = peaks_and_valleys(data)
    
    # Calculate slope for peaks and valleys
    peaks_slope = slope(peaks['Adj Close'].iloc[-1],peaks['Adj Close'].iloc[0],peaks.index[-1],peaks.index[0])
    valleys_slope = slope(valleys['Adj Close'].iloc[-1],valleys['Adj Close'].iloc[0],valleys.index[-1],valleys.index[0])
    
    # upward trend
    drop = 0
    prev = peaks.index[0]
    for i in range(1,len(peaks),1):
        curr = peaks.index[i]
        
        if peaks.loc[curr,'Adj Close'] < peaks.loc[prev,'Adj Close']:
            drop = i
        prev = curr  
    peaks = peaks.iloc[drop:]
    
    prev = valleys.index[0]
    for i in range(1,len(valleys),1):
        curr = valleys.index[i]
        
        if valleys.loc[curr,'Adj Close'] < valleys.loc[prev,'Adj Close']:
            drop = i
        prev = curr  
    valleys = valleys.iloc[drop:]
    
    # downward trend

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
