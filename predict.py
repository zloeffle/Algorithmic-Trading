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
from LinearRegression import *
from KNN import *
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
    def create_features(self,tickers,start,end,validation_date):
        df = pd.DataFrame(index=tickers)
        
        for t in tickers:
            data = client.get_historicals(t)

            # get start and end prices
            valid_price = data.loc[validation_date,'Adj Close']
            start_price = data.loc[end,'Adj Close']
            
            # generate features
            data = data.loc[:end,:]
            df.loc[t,'SMA'] = simple_moving_average(data)
            df.loc[t,'MA'] = moving_average(data)
            df.loc[t,'MACD'] = moving_average_cd(data)
            df.loc[t,'Actual Signal'] = valid_price > start_price
        return df

if __name__ == '__main__':
    s = Signal()
    #df = client.get_historicals('MSFT')
    stocks = ['MSFT','AAPL','AAL','DIS','GE']
    start = '2020-05-01'
    end = '2020-05-29'
    valid = '2020-06-05'

    s.create_features(stocks,start,end,valid)
    
        