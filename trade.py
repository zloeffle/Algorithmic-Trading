import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime

from utilities import *
from robinhood import *

import matplotlib.pyplot as plt

client = Robinhood()

'''
Common trading strategies & ML algorithms for generating BUY/SELL signals
'''
class Trader:           

    def __init__(self,cash):
        self.cash = cash
        self.history = {}
        
    def generate_features(self,stock,start,end):
        data = yf.download(stock,period='2y') # retrieve 1 years worth of historical data from yahoo finance
        results = pd.DataFrame(index=data.loc[start:end].index) # set dates as index for result dataframe

        # add signal feature to result dataframe
        temp = data.loc[start:end,:] 
        for row in temp.index:
            rsi = relative_strength_index(data.loc[:row,:])
            #mfi = money_flow_index(data.loc[:row,:])
            rsi_sig = rsi_signal(rsi)
            #mfi_sig = mfi_signal(mfi)
            
            results.loc[row,'RSI SIGNAL'] = rsi_sig
            results.loc[row,'RSI'] = rsi
            #results.loc[row,'MFI SIGNAL'] = mfi_sig
            #results.loc[row,'MFI'] = mfi

        # add adjusted closing prices for our date range to result dataframe
        results['ADJ CLOSE'] = temp['Adj Close']
        results = results.round(2)
        return results
    
    
    def backtest(self,stocks,start,end):
        data = {}
        for s in stocks:
            results = self.generate_features(s,start,end)
            print(s,results)
            print()
            results.to_csv('backtesting/2020/' + s + '.csv')


if __name__ == '__main__':
    trader = Trader(500)
    start = '2020-06-01'
    end = '2020-07-26'
    
    #tickers = client.get_collection('upcoming-earnings')
    #tickers = ['TWTR','GE','LYFT','UBER','SNAP']
    #tickers = ['XOM','CVX','ENB','ET','BP']
    tickers = [input('Enter ticker: ')]
    
    trader.backtest(tickers,start,end)
        
    