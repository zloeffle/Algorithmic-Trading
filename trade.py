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
    def generate_features(self,stock,start,end,short_ma,long_ma):
        # check that historical data for input stock can be found
        try:
            dates = yf.download(stock,start=start,end=end,period='2y').index
            dates = dates.to_pydatetime()
        except:
            print('%s not found' % stock)
            return None

        # download historical data and create the resultant dataframe
        data = yf.download(stock,end=end,period='2y').round(2)
        results = pd.DataFrame(columns=['PRICE','SHORT-MA','LONG-MA','BB-SIGNAL','RSI','TREND'],index=dates)
        
        # get price and signal features for each date
        for d in dates:
            price = data.loc[d,'Adj Close']

            # short and long simple moving averages
            short_sma = simple_moving_average(data,short_ma,d)
            long_sma = simple_moving_average(data,long_ma,d)
            
            # relative strength index
            rsi = relative_strength_index(data.loc[:d,:])

            # bollinger bands signal
            bb = bollinger_bands(data.loc[:d,:])
            bb_signal = bollinger_bands_signal(bb)

            # overall trend from the start date until the current date
            trend = trend_direction(data,start,d)
            
            # insert row into result dataframe
            results.loc[d,:] = [price,short_sma,long_sma,int(bb_signal),rsi,trend]

        results['DATE'] = results.index
        return results

    '''
    Simulate a trading scenario for a list of stocks over a specified date range

    Params
    - stocks: list of ticker symbols
    - start: start date
    - end: end date

    Returns
    - dataframe that shows the ticker, price, RSI score, recommended action, and profit from selling the stock on each respective date
    '''
    def simulate(self,stocks,start,end,short_ma,long_ma):
        portfolio = {}

        # initialize columns for result dataframe
        trade_history = pd.DataFrame(columns=['DATE','TICKER','PRICE','RSI','ACTION','PROFIT'])

        # get date range for simulation
        dates = self.generate_features(stocks[0],start,end,short_ma,long_ma).index

        i = 0
        # generate feature data for each stock
        for stock in stocks:
            data = self.generate_features(stock,start,end,short_ma,long_ma)

            for date in data.index:
                # generate the approporiate action for each date from the signal features
                price = data.loc[date,'PRICE']
                action = self.signal(data,date)
                profit = 0

                # BUY
                if action == 'BUY':
                    if stock not in portfolio:
                        portfolio[stock] = {'date':date,'price':data.loc[date,'PRICE'],'rsi':data.loc[date,'RSI']}

                # SELL
                if action == 'SELL':
                    if stock in portfolio:
                        profit = price - portfolio[stock]['price']
                        portfolio.pop(stock)
                
                # reformat date and insert row into result dataframe
                date = date.to_pydatetime().strftime('%Y-%m-%d')
                trade_history.loc[i,:] = [date,stock.upper(),price,data.loc[date,'RSI'],action,round(profit,2)]
                i += 1
        
        # compute total profit and sort rows by date
        profit = round(trade_history['PROFIT'].sum(),2)
        trade_history['DATE'] = pd.to_datetime(trade_history['DATE'])
        trade_history = trade_history.sort_values('DATE')
        #trade_history.to_csv('Backtesting/1/consumer-2019.csv',index=False)
        return trade_history,profit

    def signal(self,data,date):
        action = 'HOLD'

        price = data.loc[date,'PRICE']
        short_ma = data.loc[date,'SHORT-MA']
        long_ma = data.loc[date,'LONG-MA']
        rsi = data.loc[date,'RSI']
        signal_bb = data.loc[date,'BB-SIGNAL']
        trend = data.loc[date,'TREND']

        # BUY
        if short_ma > long_ma and short_ma > price:
            action = 'BUY'
        
        # SELL 
        if rsi > 85:
            action = 'SELL'

        return action

if __name__ == '__main__':
    trader = Trader()
    
    start = datetime(2019,1,1).strftime('%Y-%m-%d')
    end = datetime(2019,2,1).strftime('%Y-%m-%d')
    data = yf.download('msft',period='2y')
    #data = data.loc[start:end,:]
    #print(data.iloc[0])
    #print(data)
    t = trend_direction(data,start,end)
    