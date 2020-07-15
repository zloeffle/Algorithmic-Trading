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
            #df.loc[t,'MA Cross'] = moving_avg_cross(data,14,28)
            #df.loc[t,'Golden MA Cross'] = moving_avg_cross(data,50,200)
            #df.loc[t,'Mean Reversion'] = mean_reversion(data)
            #df.loc[t,'Turtle'] = turtle(data)
            
            '''
            df.loc[t,'5 Day SMA'] = simple_moving_average(data,5)
            df.loc[t,'10 Day SMA'] = simple_moving_average(data,10)
            df.loc[t,'14 Day SMA'] = simple_moving_average(data,14)
            df.loc[t,'28 Day SMA'] = simple_moving_average(data,28)
            df.loc[t,'50 Day SMA'] = simple_moving_average(data,50)
            df.loc[t,'200 Day SMA'] = simple_moving_average(data,200)
            '''
            
            df.loc[t,'Profit'] = end_price > start_price
            
        df = df.round(2)
        return df

    def decision_tree(self,df):        
        model = DecisionTree(max_depth=50)
        root = model.build_tree(df,10)
        model.print(root)
        
        
if __name__ == '__main__':
    t = Trader()
    train = pd.read_csv('train.csv',index_col='Ticker')    
    tickers = list(train.index)
    start = '2020-07-01'
    end = '2020-07-10'
    df = t.create_features(tickers,start,end)
    print(df)
    #for col in df.columns[:-1]:
    #    print('Error for %s = %d' % (col,sum(df[col] == df['Profit'])))
    