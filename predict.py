import os
import pandas as pd
import numpy as np
import math
import random
import json
from datetime import date

from utilities import *
from robinhood import *
from perceptron import *
from LinearRegression import *
from KNN import *
from DecisionTree import * 

import matplotlib.pyplot as plt

client = Robinhood()
        
'''
Common trading strategies & ML algorithms that generate buy signals and predict a stocks return 14days ahead
'''
class Signal:           
    
    '''
    Generate features using indicators from utilities.py
    '''
    def create_features(self,tickers,end,validation_date):
        df = pd.DataFrame(index=tickers)
        
        for t in tickers:
            data = client.get_historicals(t)

            # 
        return df

if __name__ == '__main__':
    s = Signal()
    df = pd.read_csv('testing.csv',index_col='Ticker')
    stocks = list(df.index)
    print(stocks)