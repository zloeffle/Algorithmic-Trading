import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
from robinhood import *
from db import *

import matplotlib.pyplot as plt
path = r"C:\Users\zloef\db\trading.db"
client = Robinhood()
db = Database(path)
 
class Trader:            
    '''
    Creates dataframe showing trading signals and price for a stock on each date in the specified range
    stock: ticker
    start: start date
    end: end date
    '''
    def generate_features(self,stock,start,end):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='1y').round(2)
        results = pd.DataFrame(columns=['PRICE','RSI','RSI-SIGNAL','BB-SIGNAL'],index=dates)
        for d in dates:
            price = data.loc[d,'Adj Close']
            
            rsi = relative_strength_index(data.loc[:d,:])
            rsi_sig = rsi_signal(rsi)

            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)
    
            results.loc[d,:] = [price,rsi,rsi_sig,int(bb_signal['SIGNAL'])]
            
        results['DATE'] = results.index
        return results

    def get_stocks(self,stocks,start,end):
        to_buy = {}
        to_sell = {}

        for stock in stocks:
            data = self.generate_features(stock,start,end)
            if data is not None:
                for date in data.index:
                    rsi = data.loc[date,'RSI-SIGNAL']
                    bb = data.loc[date,'BB-SIGNAL']

                    # BUY
                    if rsi == 1 and bb == 1:
                        if stock not in to_buy:
                            date = date.to_pydatetime().strftime('%Y-%m-%d')
                            to_buy[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}
                    # SELL
                    if rsi == -1 and bb == -1:
                        if stock in to_buy:
                            date = date.to_pydatetime().strftime('%Y-%m-%d')
                            to_sell[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}
                            
        return to_buy,to_sell

    def simulate(self,stocks,start,end,cash):
        portfolio = {}
        portfolio_value = 0
        total_value = 0
        trade_history = pd.DataFrame(columns=['DATE','TICKER','PRICE','RSI','ACTION','PROFIT'])
        to_buy,to_sell = self.get_stocks(stocks,start,end)

        i = 0
        for stock in to_buy:
            data = to_buy[stock]
            portfolio[stock] = data
            cash -= data['price']
            portfolio_value += data['price']
            trade_history.loc[i,:] = [data['date'],stock,data['price'],data['rsi'],'BUY',0]                
            i += 1
        
        for stock in to_sell:
            data = to_sell[stock]
            portfolio_value -= portfolio[stock]['price']
            portfolio.pop(stock)
            cash += data['price']
            profit = data['price']-to_buy[stock]['price']
            trade_history.loc[i,:] = [data['date'],stock,data['price'],data['rsi'],'SELL',profit]
            i += 1

        portfolio_value = round(portfolio_value,2)
        total_value = portfolio_value + cash
        total_profit = trade_history['PROFIT'].sum()
        print(trade_history)
        print(portfolio)
        print('Portfolio value: %.2f' % (portfolio_value))
        print('Cash: %.2f' % (cash))
        print('Total Value: %.2f' % (total_value))
        print('Total Profit: %.2f' % (total_profit))
        trade_history.to_csv('data/health.csv')
        return trade_history,portfolio,portfolio_value,cash,total_value,total_profit

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2020,8,3).strftime('%Y-%m-%d')
    end = datetime(2020,9,1).strftime('%Y-%m-%d')
    tickers = client.get_collection('health')
    print(len(tickers))
    trader.simulate(tickers,start,end,1000)
