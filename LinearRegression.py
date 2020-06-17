import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

'''
Goal: minimize the vertical dist between all the data points and our line
Mean Absolute Error is the easiest to understand, because it's the average error.
Mean Squared Error is more popular than MAE, because MSE "punishes" larger errors, which tends to be useful in the real world.
Root Mean Squared Error is even more popular than MSE, because RMSE is interpretable in the "y" units.
'''

class LinearRegression:
    def __init__(self,data):
        self.columns = []
        self.coef = [] # beta values
        
    def explore_data(self,data):
        print(data.info())
        print(data.describe())
        print(list(data.columns))

    '''
    params: data = pandas dataframe, features = features to drop from dataset, target = target feature in dataset
    returns: tuple(x,y) where x = dataframe of independent vars and y = dataframe of dependent vars
    '''
    def prepare_data(self,data,features,target):
        # remove irrelevant features
        data.drop(features,axis=1,inplace=True)
        
        # get target column
        y = data[target]
        
        # get predictor vars
        data.drop(target,axis=1,inplace=True)
        x = data

        # set global column list
        self.columns = list(x.columns)
        
        return x,y
    
    '''
    Splits data into training and testing components
    params: x = dataframe of predictor vars, y = dataframe of target vars, size = test size
    '''
    def train_test_split(self,x,y,size):
        split_point = int(len(x) * size)      
        x_train,y_train = x.iloc[:split_point].to_numpy(),y.iloc[:split_point].to_numpy()
        x_test,y_test = x.iloc[split_point:].to_numpy(),y.iloc[split_point:].to_numpy()
        return x_train,y_train,x_test,y_test

    def reshape_x(self,x):
        x = x.reshape(-1,1)
        return x
    
    def ones(self,x):
        ones = np.ones(shape=x.shape[0]).reshape(-1,1)
        ones = np.concatenate((ones,x),1)
        return ones

    '''
    Generates coefficients using the equation: b = (x_T dot x)^-1 dot x_T dot y
    params: x = training data for independent vars, y = training data for dependent vars
    returns: Nothing, sets adds coefficients to global array
    '''
    def fit(self,x,y):
        if (len(x.shape)) == 1:
            x = self.reshape_x(x)
        self.coef = np.linalg.inv(x.transpose().dot(x)).dot(x.transpose()).dot(y)
    
    '''
    Validate regression model and make new predictions
    params: x_test = testing data for independent vars, y_test = testing data for dependent vars
    returns: dataframe with same features as x_test as well as columns for predicted and actual values
    '''
    def predict(self,x_test,y_test):
        predictions = []
        b0 = self.coef[0]
        betas = self.coef[1:]
        
        for row in x_test:
            pred = b0
            for xi,bi in zip(row,betas):
                pred += xi*bi
            predictions.append(round(pred,2))
        
        x_test = pd.DataFrame(x_test,columns=self.columns)
        x_test['Actual'] = y_test
        x_test['Predicted'] = predictions
        return x_test