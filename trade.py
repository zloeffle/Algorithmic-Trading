import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date

from utilities import *
from robinhood import *
from db import *

import matplotlib.pyplot as plt
path = r"C:\Users\zloef\db\test.db"
client = Robinhood()
db = Database(path)
 
'''
Common trading strategies & ML algorithms for generating BUY/SELL signals
'''
class Trader:           
        
    def generate_features(self,stock,start,end):
        data = yf.download(stock,period='2y') # retrieve 1 years worth of historical data from yahoo finance
        results = pd.DataFrame(index=data.loc[start:end].index) # set dates as index for result dataframe
        #results = {}
        
        # add signal feature to result dataframe
        temp = data.loc[start:end,:] 
        for row in temp.index:
            rsi = relative_strength_index(data.loc[:row,:])
            rsi_sig = rsi_signal(rsi)
            
            results.loc[row,'RSI SIGNAL'] = rsi_sig
            results.loc[row,'RSI'] = rsi

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

    def simulate(self,stocks,start,end,cash):
        dates = self.generate_features(stocks[0],start,end).index
        records = {}
        portfolio = []

        i = 0
        for date in dates:
            for stock in stocks:
                res = self.generate_features(stock,start,date)
                print(stock)
                
                try:
                    # data to write to db
                    date = str(date)
                    price = res['ADJ CLOSE'].iloc[-1]
                    rsi = res['RSI'].iloc[-1]
                    rsi_sig = res['RSI SIGNAL'].iloc[-1]
                    action = 'HOLD'

                    # buy signal
                    if rsi_sig == 1:
                        action = 'BUY'
                    elif rsi_sig == -1:
                        action = 'SELL'

                    records[i] = [date,stock,price,rsi,rsi_sig,action]
                except:
                    continue
                i += 1
    
        results = pd.DataFrame.from_dict(records,orient='index',columns=['date','ticker','price','rsi','rsi signal','action'])
        results.to_sql('trade_history1',con=db.conn,if_exists='replace',index=False)               
        
if __name__ == '__main__':
    trader = Trader()
    
    start = '2020-07-01'
    end = '2020-07-31'
    
    tickers = client.get_collection('most-popular-under-25')
    #trader.backtest(tickers,start,end)
    trader.simulate(tickers,start,end,500)
    