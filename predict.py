import os
import pandas as pd
import numpy as np
import math
import random
import json
from datetime import date

from utilities import *
from robinhood import *
from perceptron import *
from DecisionTree import * 

import matplotlib.pyplot as plt

client = Robinhood()
        
'''
Common trading strategies & ML algorithms that generate buy signals and predict a stocks return 14days ahead
'''
class Signal:           
    
    '''
    Generate features using indicators from utilities.py
    '''
    def create_features(self,tickers,start,end):
        df = pd.DataFrame(index=tickers)
        
        for t in tickers:
            data = client.get_historicals(t)
            
            # prices
            start_price = data.loc[start,'Adj Close']
            end_price = data.loc[end,'Adj Close']
            
            data = data.loc[:start,]
            
            ret = weekly_return(data)
            rsi = relative_strength_index(data)
            mfi = money_flow_index(data)
            
        print(df)
        return df

if __name__ == '__main__':
    s = Signal()
    df = pd.read_csv('testing.csv')
    stocks = list(df['Ticker'])
    
    start = '2020-06-01'
    end = '2020-06-08'
    s.create_features(stocks,start,end)
    #df = client.get_historicals(stocks[0])
    #simple_moving_average(df,20)
    #exponential_moving_average(df,20)