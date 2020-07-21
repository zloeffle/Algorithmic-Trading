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
            
            if signal >= 70:
                results.loc[row,'SIGNAL'] = -1
            elif signal <= 30:
                results.loc[row,'SIGNAL'] = 1
            else:
                results.loc[row,'SIGNAL'] = 0    
            results.loc[row,'RSI'] = signal

        # add adjusted closing prices for our date range to result dataframe
        results['ADJ CLOSE'] = temp['Adj Close']
        results = results.round(2)
        return data,results

    def backtest(self,stock,start,end):
        portfolio = {}

        # iterate through input stocks
        data,results = self.generate_features(stock,start,end)       
    
        # iterate rows in result dataframe
        for row in results.index: 
            row = row.strftime('%Y-%m-%d')
            profit = 0

            # check for buy signal
            if results.loc[row,'SIGNAL'] == 1:
                print(stock)
                print(portfolio)
                print(results.loc[:row,:])
                shares = int(input('Enter shares to buy: '))
                
                if not stock in portfolio:           
                    portfolio[stock] = [(results.loc[row,'ADJ CLOSE'],shares)]   
                    action = 'Buying %d shares of %s' % (shares,stock)              
                else:
                    if shares == 0:
                        action = 'Not buying more shares of %s' % (stock)
                    else:
                        portfolio[stock].append((results.loc[row,'ADJ CLOSE'],shares))
                        action = 'Buying %d more shares of %s' % (shares,stock)

            # check for sell signal
            elif results.loc[row,'SIGNAL'] == -1:
                if stock in portfolio:
                    sell_price = results.loc[row,'ADJ CLOSE']
                    print(s)
                    print(portfolio)
                    print(results.loc[:row,:])
                    shares = int(input('Enter shares to sell: '))
                    if shares == 0:
                        print('Not selling anymore shares of %s' % (stock))
                    else:
                        tot_shares = 0
                        for item in portfolio[stock]:
                            tot_shares += item[1]
                            profit += (item[0] * item[1])
                        profit = (sell_price * tot_shares) - profit
                        action = 'Sold %s for profit of %.2f' % (stock,profit)
                        del portfolio[stock]
                else:
                    action = '%s not owned so cannot sell' % (stock)
            else:
                action = 'HOLD'
            
            results.loc[row,'ACTION'] = action
            results.loc[row,'PROFIT'] = profit
        return results,portfolio

if __name__ == '__main__':
    t = Trader(500)

    tickers = ['SNAP','BAC','UBER','KO','LUV','GM','DKNG','HUYA','LYFT']
    start = '2020-05-01'
    end = '2020-05-29'
    for s in tickers:
        res,port = t.backtest(s,start,end)
        print(res)
        print(port)
    