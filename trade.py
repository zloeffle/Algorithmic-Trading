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
        self.portfolio_value = None
    
    def generate_features(self,stock,start,end):
        data = yf.download(stock,period='1y') # retrieve 1 years worth of historical data from yahoo finance
        results = pd.DataFrame(index=data.loc[start:end].index) # set dates as index for result dataframe

        # add signal feature to result dataframe
        temp = data.loc[start:end,:] 
        for row in temp.index:
            signal = relative_strength_index(data.loc[:row,:])
            #results.loc[row,'RSI'] = signal
            
            if signal >= 70:
                results.loc[row,'SIGNAL'] = -1
            elif signal <= 30:
                results.loc[row,'SIGNAL'] = 1
            else:
                results.loc[row,'SIGNAL'] = 0    
            
        # add adjusted closing prices for our date range to result dataframe
        results['ADJ CLOSE'] = temp['Adj Close']
        results = results.round(2)
        return data,results
    
    def backtest(self,stock,start,end):
        portfolio = {}
        portfolio_value = 0
        
        # iterate through input stocks
        data,results = self.generate_features(stock,start,end)       
    
        # iterate rows in result dataframe
        for row in results.index: 
            row = row.strftime('%Y-%m-%d')
            #action = None
            
            # check for buy signal
            if results.loc[row,'SIGNAL'] == 1:
                # if current stock is not in portfolio, add it and adjust cash balance/portfolio value according to purchase price
                if not stock in portfolio:                        
                    portfolio[stock] = [results.loc[row,'ADJ CLOSE']]
                    portfolio_value += results.loc[row,'ADJ CLOSE']
                    self.cash -= results.loc[row,'ADJ CLOSE']
                    
                    action = 'Buying %s for %.2f' % (stock,results.loc[row,'ADJ CLOSE'])
                else:
                    # calculate how many shares to purchase
                    portfolio[stock].append(results.loc[row,'ADJ CLOSE'])
                    portfolio_value += results.loc[row,'ADJ CLOSE']
                    self.cash -= results.loc[row,'ADJ CLOSE']
                    
                    action = 'Buying more %s for %.2f' % (stock,results.loc[row,'ADJ CLOSE'])

            # check for sell signal
            elif results.loc[row,'SIGNAL'] == -1:
                if stock in portfolio:
                    profit = results.loc[row,'ADJ CLOSE']*len(portfolio[stock]) - sum(portfolio[stock])
                    self.cash += results.loc[row,'ADJ CLOSE']*len(portfolio[stock])
                    portfolio_value -= sum(portfolio[stock])
                    del portfolio[stock]
                    
                    action = 'Selling %s for $%.2f profit = %.2f' % (stock,results.loc[row,'ADJ CLOSE'],profit)
                else:
                    action = '%s not owned so cannot sell' % (stock)
            else:
                action = 'HOLD'
            
            results.loc[row,'ACTION'] = action
            results.loc[row,'RSI'] = relative_strength_index(data.loc[:row])
            results.loc[row,'CASH'] = self.cash
        return results,portfolio

if __name__ == '__main__':
    t = Trader(500)

    train = pd.read_csv('train.csv',index_col='Ticker')    
    tickers = list(train.index)

    res,port = t.backtest(tickers[10],'2020-06-01','2020-07-17')
    print(res)
    print(port)