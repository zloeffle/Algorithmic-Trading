import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import random

'''
Goal: minimize the vertical dist between all the data points and our line
Mean Absolute Error is the easiest to understand, because it's the average error.
Mean Squared Error is more popular than MAE, because MSE "punishes" larger errors, which tends to be useful in the real world.
Root Mean Squared Error is even more popular than MSE, because RMSE is interpretable in the "y" units.
'''

class LinearRegression:
    def __init__(self):
        self.coef = [] # beta values
    
    '''
    Splits data into training and testing components
    params: x = dataframe of predictor vars, y = dataframe of target vars, size = test size
    '''
    def train_test_split(self,x,y,split):      
        x_train,y_train = x.loc[:split,],y.loc[:split,]
        x_test,y_test = x.loc[split:,],y.loc[split:,]
        return x_train,y_train,x_test,y_test
    
    def ones(self,x):
        ones = np.ones(shape=x.shape[0]).reshape(-1,1)
        return np.concatenate((ones,x),1)

    '''
    Generates coefficients using the equation: b = (x_T dot x)^-1 dot x_T dot y
    params: x = training data for independent vars, y = training data for dependent vars
    returns: Nothing, sets adds coefficients to global array
    '''
    def fit(self,x,y):
        # add col of ones to x matrix
        x = self.ones(x)

        # generate coeficients 
        coef = np.linalg.inv(x.transpose().dot(x)).dot(x.transpose()).dot(y)
        self.coef = coef
    
    '''
    Validate regression model and make new predictions
    params: x_test = testing data for independent vars, y_test = testing data for dependent vars
    returns: dataframe with same features as x_test as well as columns for predicted and actual values
    '''
    def predict(self,x_test,y_test):
        preds = [] # predictions
        b0 = self.coef[0]
        betas = self.coef[1:]
        x_test = self.ones(x_test)

        for row in x_test:
            pred = b0
            for xi,bi in zip(row,betas):
                pred += xi*bi
            preds.append(pred)
        return preds