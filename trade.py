import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import date

from utilities import *
from network import *

import matplotlib.pyplot as plt
        
'''
Common trading strategies & ML algorithms that generate buy signals and predict a stocks return 14days ahead
'''
class Trader:           
    
    '''
    Generate features using indicators from utilities.py
    '''
    def create_features(self,tickers,start_date,end_date):
        df = pd.DataFrame(index=tickers)
        
        for t in tickers:
            data = yf.download(t,period='1y')

            # use data only up to start date for feature generation
            temp = data.loc[:start_date,:]
            
            # features
            df.loc[t,'SMA Cross'] = simple_moving_avg_cross(temp,20,30)
            df.loc[t,'EMA Cross'] = exponential_moving_avg_cross(temp,20,30)
            df.loc[t,'Mean Reversion'] = mean_reversion(temp)
            #df.loc[t,'RSI'] = relative_strength_index(data)
            #df.loc[t,'MFI'] = money_flow_index(data)
            
            #df.loc[t,'5 Day SMA'] = simple_moving_average(temp,5)
            #df.loc[t,'10 Day SMA'] = simple_moving_average(temp,10)
            #df.loc[t,'20 Day SMA'] = simple_moving_average(temp,20)
            #df.loc[t,'40 Day SMA'] = simple_moving_average(temp,40)
            
            df.loc[t,'START OF WEEK ADJ CLOSE'] = data.loc[start_date,'Adj Close']
            df.loc[t,'END OF WEEK ADJ CLOSE'] = data.loc[end_date,'Adj Close']
            df.loc[t,'PROFIT'] = df.loc[t,'START OF WEEK ADJ CLOSE'] < df.loc[t,'END OF WEEK ADJ CLOSE']
        
        df = df.round(2)
        return df
        
    def ANN(self,data):
        pass        

    def backtest(self,stocks,start,end):
        results = pd.DataFrame()

        for s in stocks:
            data = yf.download(s,period='1y')
            data = data.loc[:end,:]
            dates = data.loc[start:end,:].index
            
            for date in dates:
                
            break
            
if __name__ == '__main__':
    t = Trader()

    train = pd.read_csv('train.csv',index_col='Ticker')    
    tickers = list(train.index)[:10]
    
    t.backtest(tickers,'2020-06-01','2020-06-30')
    