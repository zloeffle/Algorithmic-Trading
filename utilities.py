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
Finds the peaks and valleys for a stock's historical price data over a specified period
'''
def peaks_and_valleys(data,period=21):
    df = data.copy()
    df = df[['Adj Close','High','Low']].round(2)
    #df = df.iloc[-period:]
    df['date_id'] = range(1,len(df)+1)

    # set index as integer scale
    df['DATE'] = df.index
    df.index = df['date_id']
    print(df)
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
    
    print(peaks,valleys)
    return list(peaks['Adj Close']),list(valleys['Adj Close'])

'''
Calculates the slope and y intercept for the line of best fit that represents the given data points
'''
def best_fit(x,y):
        n = len(x)
        x_bar = sum(x)/n
        y_bar = sum(y)/n
        
        numer = n*sum([xi*yi for xi,yi in zip(x,y)]) - (sum(x)*sum(y))
        denom = n*sum([xi**2 for xi in x]) - sum(x)**2
        slope = round(numer/denom,2)
        b = (sum(y) - slope*sum(x))/n
        return slope,b

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
