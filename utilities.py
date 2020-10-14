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
Finds the peaks and valleys for a stock's historical price data over a specified period
'''
def peaks_and_valleys(data,period):
    df = data.copy()
    df = df[['Adj Close','High','Low']].round(2)
    df = df.iloc[-period:]
    df['date_id'] = range(1,len(df)+1)
    #print(df)
    
    # set index as integer scale
    df.index = df['date_id']
    
    # Get peaks and valleys to compute trend direction
    peaks = []
    valleys = []
    thresh = 1
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

'''
Computes upward and downward trend lines as well as their slopes
'''
def trend_direction(data,periods=21,plot=False):
    peaks,valleys = peaks_and_valleys(data,periods)
    peaks = peaks.sort_values('Adj Close')
    valleys = valleys.sort_values('Adj Close')

    '''
    Lowest Peak and Highest peak
    Lowest valley and Highest valley
    *** LOWEST MUST COME AFTER HIGHEST OR HIGHEST MUST COME AFTER LOWEST
    '''
    highs = [peaks.index[0],peaks.index[-1]]
    lows = [valleys.index[0],valleys.index[-1]]
    highs.sort()
    lows.sort()

    # Slope for peaks and valleys
    peaks_slope = slope(peaks.loc[highs[-1],'Adj Close'],peaks.loc[highs[0],'Adj Close'],highs[-1],highs[0])
    valleys_slope = slope(valleys.loc[lows[-1],'Adj Close'],valleys.loc[lows[0],'Adj Close'],lows[-1],lows[0])

    # y intercepts for peaks and valleys
    valleys_y_int = valleys.loc[lows[-1],'Adj Close'] - valleys_slope*lows[-1]
    peaks_y_int = peaks.loc[highs[-1],'Adj Close'] - peaks_slope*highs[-1]

    # generate upward and downward trendlines
    valleys_trend_line,peaks_trend_line = [],[]
    x = range(1,periods+1)
    y = np.array(data['Adj Close'].iloc[-periods:].round(2))
    for val in x:
        down = round(peaks_slope*val + peaks_y_int,2)
        up = round(valleys_slope*val + valleys_y_int,2)
        valleys_trend_line.append(up)
        peaks_trend_line.append(down)

    if plot:
        plt.plot(x,y,color='b')
        plt.xticks(np.arange(min(x),max(x)+1,1.0))

        plt.plot(x,valleys_trend_line,color='r')
        plt.plot(x,peaks_trend_line,color='g')

        plt.grid()
        plt.show()

    price = data['Adj Close'].iloc[-1]
    ma = data['Adj Close'].rolling(5).mean().round(2)
    ma = ma.iloc[-5:]
    
    return peaks_slope,valleys_slope
    '''
    # UPTREND 
    if valleys_slope > 0:
        if price > max(valleys_trend_line):
            if ma.iloc[-1] > ma.iloc[0] and price >= ma.iloc[-1]:
                return 'UP'
            else:
                return 'UP REVERSING'
        else:
            return 'UP REVERSING'

    # DOWNTREND
    elif peaks_slope < 0:
        if price < min(peaks_trend_line):
            if ma.iloc[-1] < ma.iloc[0] and price <= ma.iloc[-1]:
                return 'DOWN'
            else:
                return 'DOWN REVERSING'
        else:
            return 'DOWN REVERSING'
    # FLAT TREND
    else:
        return 'FLAT
    '''


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
