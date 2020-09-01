import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
from robinhood import *
from db import *

import matplotlib.pyplot as plt
path = r"C:\Users\zloef\db\trading.db"
client = Robinhood()
db = Database(path)
 
class Trader:            
    '''
    Creates dataframe showing trading signals and price for a stock on each date in the specified range
    stock: ticker
    start: start date
    end: end date
    '''
    def generate_features(self,stock,start,end):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='1y').round(2)
        results = pd.DataFrame(columns=['PRICE','RSI','RSI-SIGNAL','BB-SIGNAL'],index=dates)
        for d in dates:
            price = data.loc[d,'Adj Close']
            
            rsi = relative_strength_index(data.loc[:d,:])
            rsi_sig = rsi_signal(rsi)

            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)
    
            results.loc[d,:] = [price,rsi,rsi_sig,int(bb_signal['SIGNAL'])]
            
        results['DATE'] = results.index
        return results

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2020,8,3).strftime('%Y-%m-%d')
    end = datetime(2020,8,28).strftime('%Y-%m-%d')
    tickers = client.get_collection('finance')
    cash = 500

    trader.backtest(tickers,start,end,cash)