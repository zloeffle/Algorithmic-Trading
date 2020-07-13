import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import date

from utilities import *
from DecisionTree import * 

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
            data = yf.download(t,end=end_date,period='2y')

            # validate future price
            start_price = data.loc[start_date,'Adj Close']
            end_price = data.loc[end_date,'Adj Close']

            # use data only up to start date for feature generation
            data = data.loc[:start_date,:]
            
            # features
            df.loc[t,'RSI'] = relative_strength_index(data)
            df.loc[t,'MFI'] = money_flow_index(data)
            df.loc[t,'MA Cross'] = moving_avg_cross(data,5,20)
            df.loc[t,'Profit'] = end_price > start_price

        df = df.round(2)
        return df


if __name__ == '__main__':
    t = Trader()
    train = pd.read_csv('train.csv',index_col='Ticker')
    test1 = pd.read_csv('test1.csv',index_col='Ticker')
    test2 = pd.read_csv('test2.csv',index_col='Ticker')
    test3 = pd.read_csv('test3.csv',index_col='Ticker')
    
    tickers = list(train.index)
    start = '2020-06-01'
    end = '2020-06-05'
    df = t.create_features(tickers,start,end)
    