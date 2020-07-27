import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime

from utilities import *
from network import *
from robinhood import *

import matplotlib.pyplot as plt

client = Robinhood()

'''
Common trading strategies & ML algorithms for generating BUY/SELL signals
'''
class Trader:           

    def __init__(self,cash):
        self.cash = cash
        self.portfolio = None
        self.watchlist = []
        self.portfolio_value = None
        
    def generate_features(self,stock,start,end):
        data = yf.download(stock,period='2y') # retrieve 1 years worth of historical data from yahoo finance
        results = pd.DataFrame(index=data.loc[start:end].index) # set dates as index for result dataframe

        # add signal feature to result dataframe
        temp = data.loc[start:end,:] 
        for row in temp.index:
            rsi = relative_strength_index(data.loc[:row,:])
            mfi = money_flow_index(data.loc[:row,:])
            rsi_sig = rsi_signal(rsi)
            mfi_sig = mfi_signal(mfi)
            
            results.loc[row,'RSI SIGNAL'] = rsi_sig
            results.loc[row,'RSI'] = rsi
            results.loc[row,'MFI SIGNAL'] = mfi_sig
            results.loc[row,'MFI'] = mfi

        # add adjusted closing prices for our date range to result dataframe
        results['ADJ CLOSE'] = temp['Adj Close']
        results = results.round(2)
        return results
    
    
    def backtest(self,stocks,start,end):
        for s in stocks:
            results = self.generate_features(s,start,end)
            print(s,results)
            print()

if __name__ == '__main__':
    trader = Trader(500)
    start = '2019-06-03'
    end = '2019-07-21'
    
    #tickers = client.get_collection('100-most-popular')
    tickers = ['TWTR','F','GE','LYFT','UBER','CHWY']
    trader.backtest(tickers,start,end)
        
    