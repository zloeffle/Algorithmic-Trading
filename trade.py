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
            df.loc[t,'MA Cross'] = moving_avg_cross(temp,10,30)
            df.loc[t,'Mean Reversion'] = mean_reversion(temp)
            #df.loc[t,'RSI'] = relative_strength_index(data)
            #df.loc[t,'MFI'] = money_flow_index(data)
            df.loc[t,'START OF WEEK ADJ CLOSE'] = data.loc[start_date,'Adj Close']
            df.loc[t,'END OF WEEK ADJ CLOSE'] = data.loc[end_date,'Adj Close']
            df.loc[t,'PROFIT'] = df.loc[t,'START OF WEEK ADJ CLOSE'] < df.loc[t,'END OF WEEK ADJ CLOSE']

        df = df.round(2)
        return df
        
    def ANN(self,data):
        pass        

    def backtest(self,stocks,month):
        results = pd.DataFrame()

        for week in month:
            end = pd.date_range(start=week,periods=5)[-1]
            print(end)
            
            data = self.create_features(stocks,week,end)
            results.loc[week,'MA CROSS ERROR'] = sum(data['MA Cross'] == data['PROFIT'])
            results.loc[week,'MEAN REVERSION ERROR'] = sum(data['Mean Reversion'] == data['PROFIT'])
        print(results)
if __name__ == '__main__':
    t = Trader()

    train = pd.read_csv('train.csv',index_col='Ticker')    
    tickers = list(train.index)
    
    june = ['2020-06-01','2020-06-08','2020-06-15','2020-06-22','2020-06-29']
    july = ['2020-07-06','2020-07-13']
    t.backtest(tickers,june)
