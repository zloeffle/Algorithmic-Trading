import os
import pandas as pd
import numpy as np
import math
from datetime import date

from utilities import *
#from robinhood import *
from perceptron import *
#from LinearRegression import *

import matplotlib.pyplot as plt

#client = Robinhood()
        
'''
Common trading strategies & ML algorithms that generate buy signals and predict a stocks return 14days ahead
'''
class Signal:
    def __init__(self,data):
        self.portfolio = data
        self.results = {}           
    
    '''
    Generate features using indicators from utilities.py
    '''
    def create_features(self,data,end_date='2020-05-29',future_date='2020-06-05'):
        df = self.portfolio
        
        for t in list(df.index):
            # historical data
            hist = client.get_historicals(t)
            
            # past and future prices
            try:
                past_price = hist.loc[end_date,'Adj Close']
                future_price = hist.loc[future_date,'Adj Close']
            except KeyError:
                continue
                
            # signals
            sma = simple_moving_average(hist,end_date) # simple MA 
            ma = moving_average(hist,end_date) # MA
            mac = macd(hist,end_date) # MACD
            rsi = relative_strength_index(hist,end_date) # RSI
            
            # add features for each stock
            df.loc[t,'Simple MA'] = sma
            df.loc[t,'MA'] = ma
            df.loc[t,'MACD'] = mac
            df.loc[t,'RSI'] = rsi
            df.loc[t,'7-Day Profit']  = future_price > past_price

        df.dropna(inplace=True,axis=0)
        return df

    '''
    Implementation of the MLP model
    
    Params: Dataframe of stocks and technical indicators
    Returns: tuple(Input dataframe with columns for actual and predicted values, MLP model object)
    '''
    def mlp_network(self,df):
        df.set_index('Ticker',inplace=True)
        columns = list(df.columns)
        
        # set target classifications
        target = df[str(columns[-1])]
        df.drop(str(columns[-1]),axis=1,inplace=True)
        
        # set input data and add col for bias
        inputs = df
        inputs['Bias'] = 1
        
        # initialize mlp model and train
        model = MLP(df,inputs,target)
        model.train()
        
        # generate outputs
        out = [model.predict(p) for p in model.inputs]
        df['Target'] = target
        df['Target'] = df['Target'].astype(int)
        df['Output'] = out
        
        df.drop('Bias',axis=1,inplace=True)
        return df,model
    
    '''
    Generates accuracy metrics for the MLP model
    
    Params: train = dataframe to train the model, test = dataframe to test and validate the model
    Returns: 
    '''
    def mlp_evaluation(self,train,test):     
        cols = list(test.columns)
        
        # training data results
        train_results,model = self.mlp_network(train)
        
        # set our target data
        y = test[str(cols[-1])]
        y = y.to_numpy()
        test.drop(str(cols[-1]),axis=1,inplace=True)
        
        # prepare the independent variables
        x = test
        x.set_index('Ticker',inplace=True)
        x = x.to_numpy()
        
        # predict from testing data 
        print('\nTesting Data')
        out = [model.predict(p) for p in x]
        
        # Build resultant dataframe
        x = pd.DataFrame(x,index=test.index,columns=cols[1:5])
        x['Target'] = y
        x['Target'] = x['Target'].astype(int)
        x['Output'] = out
        
        print('Training Accuracy: %.2f' % round(sum(train_results['Target'] == train_results['Output'])/len(train_results) * 100,2))
        print('Testing Accuracy: %.2f' % round(sum(x['Target'] == x['Output'])/len(x) * 100,2))
        print(train_results)
        print(x)
        
if __name__ == '__main__':
    df1 = pd.read_csv('train_04-30-2020.csv')
    df2 = pd.read_csv('train_05-29-2020.csv')
    df3 = pd.read_csv('train_06-01-2020.csv')
    s = Signal(df1)
    s.mlp_evaluation(df1,df2)
        