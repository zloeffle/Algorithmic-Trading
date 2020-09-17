import os
import pandas as pd
import numpy as np
import yfinance as yf
import math
import random
import json
from datetime import datetime,date,timedelta

from utilities import *
#from db import *

import matplotlib.pyplot as plt

'''
db = Database(path)
path = r"" 
'''

class Trader:        
        
    '''
    Creates dataframe showing trading signals and price for a stock on each date in the specified range
    
    Params
    - stock: ticker for stock (string)
    - start: starting date for period (datetime)
    - end: ending date for period (datetime)
    
    Returns
    - pandas dataframe containing feature values for each date in specified range
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
        data = yf.download(stock,end=end,period='2y').round(2)
        results = pd.DataFrame(columns=['PRICE','SHORT-MA','LONG-MA','RSI','RSI-SIGNAL','BB-SIGNAL'],index=dates)
        
        # get price and signal features for each date
        for d in dates:
            price = data.loc[d,'Adj Close']
            
            rsi = relative_strength_index(data.loc[:d,:])
            rsi_sig = rsi_signal(rsi)

            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)

            # exponential
            #short_ma = exponential_moving_average(data,5,d)
            #long_ma = exponential_moving_average(data,15,d)
            short_ma = simple_moving_average(data,5,d)
            long_ma = simple_moving_average(data,15,d)

            results.loc[d,:] = [price,short_ma,long_ma,rsi,rsi_sig,int(bb_signal)]

        results['DATE'] = results.index
        return results


    '''
    Gets stocks to buy/sell for each date in the given period based on values from the signal features
    
    Params
    - stocks: list of ticker strings
    - start: starting date for period (datetime)
    - end: ending date for period (datetime)
    
    Returns
    - tuple containing 2 dictionaries for stocks that should be bought/sold (key: ticker values: date,price,signal features)
    '''
    def get_stocks(self,stocks,start,end):
        # initialize dictionaries to return
        to_buy = {}
        to_sell = {}

        # generate features for each stock
        for stock in stocks:
            data = self.generate_features(stock,start,end)
            
            # check that feature data is not null
            if data is not None:
                
                # generate action for each date in feature data
                for date in data.index:
                    rsi = data.loc[date,'RSI-SIGNAL']
                    bb = data.loc[date,'BB-SIGNAL']
                    short_ma = data.loc[date,'SHORT-MA']
                    long_ma = data.loc[date,'LONG-MA']
                    
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

    '''
    Simulate a trading scenario for a list of stocks over a specified date range

    Params
    - stocks: list of ticker symbols
    - start: start date
    - end: end date

    Returns
    - dataframe that shows the ticker, price, RSI score, recommended action, and profit from selling the stock on each respective date
    '''
    def simulate(self,stocks,start,end):
        portfolio = {}
        trade_history = pd.DataFrame(columns=['DATE','TICKER','PRICE','RSI','ACTION','PROFIT'])

        dates = self.generate_features(stocks[0],start,end).index
        i = 0
        for stock in stocks:
            data = self.generate_features(stock,start,end)

            for date in data.index:
                price = data.loc[date,'PRICE']
                rsi = data.loc[date,'RSI']
                signal_rsi = data.loc[date,'RSI-SIGNAL']
                signal_bb = data.loc[date,'BB-SIGNAL']

                action = 'HOLD'
                profit = 0
                if signal_rsi == 1 and signal_bb == 1:
                    if stock not in portfolio:
                        action = 'BUY'
                        portfolio[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}

                if signal_rsi == -1 and signal_bb == -1:
                    if stock in portfolio:
                        action = 'SELL'
                        profit = price - portfolio[stock]['price']
                        portfolio.pop(stock)
                date = date.to_pydatetime().strftime('%Y-%m-%d')
                trade_history.loc[i,:] = [date,stock.upper(),price,rsi,action,round(profit,2)]
                i += 1
        
        trade_history['DATE'] = pd.to_datetime(trade_history['DATE'])
        trade_history = trade_history.sort_values('DATE')
        trade_history.to_csv('Backtesting/1/consumer-2019.csv',index=False)
        return trade_history

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2020,8,26).strftime('%Y-%m-%d')
    end = datetime(2020,9,2).strftime('%Y-%m-%d')
    data = yf.download('msft',period='1y')

    t = trend(data,start,end)
    print(t)
    