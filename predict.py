import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import date

from utilities import *
from perceptron import *
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

            # features
            #df.loc[t,'14 Day SMA'] = simple_moving_average(data,14).loc[end_date,]
            #df.loc[t,'28 Day SMA'] = simple_moving_average(data,28).loc[end_date,]
            #df.loc[t,'14 Day EMA'] = exponential_moving_average(data,14).loc[end_date,]
            #df.loc[t,'28 Day EMA'] = exponential_moving_average(data,28).loc[end_date,]
            df.loc[t,'RSI'] = relative_strength_index(data)
            df.loc[t,'MFI'] = money_flow_index(data)
            #df.loc[t,'Start Price'] = start_price
            #df.loc[t,'End Price'] = end_price
            #df.loc[t,'Actual Profit'] = end_price-start_price
            df.loc[t,'Buy Signal'] = end_price > start_price

        df = df.round(2)
        return df


if __name__ == '__main__':
    t = Trader()
    train = pd.read_csv('train.csv',index_col='Ticker')
    test1 = pd.read_csv('test1.csv',index_col='Ticker')
    test2 = pd.read_csv('test2.csv',index_col='Ticker')
    test3 = pd.read_csv('test3.csv',index_col='Ticker')
    