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
Common trading strategies & ML algorithms for generating BUY/SELL signals
'''
class Trader:           

    def backtest(self,stocks,start,end):
        cash = 300
        portfolio = {}
        portfolio_value = 0

        # iterate through input stocks
        for s in stocks:
            data = yf.download(s,period='1y') # retrieve 1 years worth of historical data from yahoo finance
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
                
            # add adjusted closing prices for our date range to result dataframe
            results['ADJ CLOSE'] = temp['Adj Close']
            results = results.round(2)

            print(s)
            print(results)
            print()
            # iterate rows in result dataframe
            for row in results.index:                
                # check for buy signal
                if results.loc[row,'SIGNAL'] == 1:
                    # if current stock is not in portfolio, add it and adjust cash balance/portfolio value according to purchase price
                    if not s in portfolio:
                        # stop if cash balance is too low
                        if cash < results.loc[row,'ADJ CLOSE']:
                            break

                        rsi = relative_strength_index(data.loc[:row,:])
                        print('RSI = %.2f and Cash = %.2f' % (rsi,cash))
                        print('Buying %s for %.2f' % (s,results.loc[row,'ADJ CLOSE']))
                        portfolio[s] = [results.loc[row,'ADJ CLOSE']]
                        portfolio_value += results.loc[row,'ADJ CLOSE']
                        cash -= results.loc[row,'ADJ CLOSE']
                    else:
                        # if stock is already owned buy more shares at the signaled price
                        print('Buying more %s for %.2f' % (s,results.loc[row,'ADJ CLOSE']))
                        
                        # calculate how many shares to purchase
                        portfolio[s].append(results.loc[row,'ADJ CLOSE'])
                        
                        portfolio_value += results.loc[row,'ADJ CLOSE']
                        cash -= results.loc[row,'ADJ CLOSE']

                # check for sell signal
                elif results.loc[row,'SIGNAL'] == -1:
                    # if stock to sell is in portfolio, calculate profit, update cash balance, update portfolio values, and remove it from the portfolio
                    if s in portfolio:
                        print('Selling %s for $%.2f' % (s,results.loc[row,'ADJ CLOSE']))
                        profit = results.loc[row,'ADJ CLOSE']*len(portfolio[s]) - sum(portfolio[s])
                        print('Profit from selling %d shares of %s = %.2f' % (len(portfolio[s]),s,profit))
                        cash += results.loc[row,'ADJ CLOSE']*len(portfolio[s])
                        portfolio_value -= sum(portfolio[s])
                        del portfolio[s]
                    else:
                        print('%s not owned so cannot sell' % (s))

        print(portfolio)
        print('Portfolio value = %.2f' % (portfolio_value))
        print('Cash balance = %.2f' % (cash))
        print()
        print()

if __name__ == '__main__':
    t = Trader()

    train = pd.read_csv('train.csv',index_col='Ticker')    
    tickers = list(train.index)
    
    t.backtest(tickers,'2020-07-01','2020-07-17')
    