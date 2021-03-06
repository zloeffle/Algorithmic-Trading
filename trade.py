import os
from time import time
import pandas as pd
import numpy as np
#from pandas.core.series import num
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
from robinhood import *
#from db import *

import matplotlib.pyplot as plt

'''
db = Database(path)
path = r"" 
'''
client = Robinhood()

class Trader:        
        
    '''
    Creates dataframe showing trading signals and price for a stock on each date in the specified range
    
    Params
    - stock: ticker for stock (string)
    - start: starting date for period (datetime)
    - end: ending date for period (datetime)
    - long_ma: window to compute long term moving average
    - short_ma: window to compute short term moving average
    
    Returns
    - pandas dataframe containing feature values for each date in specified range
    '''
    def generate_features(self,stock,start,end,short_ma=5,long_ma=25):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='2y').round(2)
        results = pd.DataFrame(columns=['PRICE','SHORT-MA','LONG-MA','BB-UPPER','BB-LOWER','BB-WIDTH','RSI','PEAKS-SLOPE','VALLEYS-SLOPE'],index=dates)
        
        # get price and signal features for each date
        for d in dates:
            price = data.loc[d,'Adj Close']

            # short and long simple moving averages
            short_sma = simple_moving_average(data,short_ma,d)
            long_sma = simple_moving_average(data,long_ma,d)
            
            # relative strength index
            rsi = relative_strength_index(data.loc[:d,:])

            # bollinger bands
            bb = bollinger_bands(data.loc[:d,:])
            bb_upper = bb.loc[d,'UPPER'] # upper band
            bb_lower = bb.loc[d,'LOWER'] # lower band
            bb_width = bb.loc[d,'WIDTH'] # width between upper and lower

            # overall trend from the start date until the current date
            peaks,valleys = peaks_and_valleys(data.loc[:d,:])
            peaks.append(price)
            valleys.append(price)
            peaks_slope = best_fit(range(1,len(peaks)+1),peaks)[0]
            valleys_slope = best_fit(range(1,len(valleys)+1),valleys)[0]
            
            # insert row into result dataframe
            results.loc[d,:] = [price,short_sma,long_sma,bb_upper,bb_lower,bb_width,rsi,peaks_slope,valleys_slope]

        results['DATE'] = results.index
        return results


    '''
    Generates buy/sell signals based on moving average, bollinger bands, relative strength index
    '''
    def signal(self,data):        
        data['ACTION'] = 'HOLD'
        data = data.reset_index(drop=True)
        low = data['PRICE'].min()
        low_index = data[data['PRICE'] == low].index.values[0]
        high = data.loc[low_index:,'PRICE'].max()
        high_index = data[data['PRICE'] == high].index.values[0]
        
        data.loc[low_index,'ACTION'] = 'BUY'
        data.loc[high_index,'ACTION'] = 'SELL'
        return data
        
        
if __name__ == '__main__':
    trader = Trader()
    client = Robinhood()
    start = datetime(2020,8,1).strftime('%Y-%m-%d')
    end = datetime(2020,9,3).strftime('%Y-%m-%d')
    data = yf.download('msft',period='2y')
    data = data.loc[:end,:]
    
    data = trader.generate_features('msft',start,end)
    print(data)