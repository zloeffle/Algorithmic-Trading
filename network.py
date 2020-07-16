import pandas as pd
import numpy as np
import random
import math

'''
Implementation of a multilayer perceptron network
'''
class Neural_Network:
    def __init__(self,inputs,targets):
        self.inputs = inputs # inputs for the mlp model
        self.targets = targets # target values
        
        self.input_size = len(self.inputs[0]) # size of each input
        self.num_inputs = len(inputs) # total number of inputs
        
        self.weights = [random.random() for _ in range(self.input_size + 1)] # initialize weights randomly
   
    def sigmoid(self,x):
        return 1/(1 + np.exp(-x))
    
    def sigmoid_derivative(self,x):
        return self.sigmoid(x) * (1-self.sigmoid(x))
    
    def mean_square_error(self,target,output):
        return 0.5 * math.pow((target-output),2)
    
    def gradient_descent(self):
        pass
    
    def train(self):
        pass
        
    def predict(self,inputs):
        z = self.dot(self.weights,inputs)
        a = self.sigmoid(z)
        #print('W*X: %f  Activation: %d' % (z,a))
        return a
        
    
    '''
    Return dot product of two vectors
    '''
    def dot(self, a, b):
        x = 0
        for i,j in zip(a,b):
            x += i*j
        return x

    '''
    Return addition of two vectors
    '''
    def add(self, a, b):
        x = []
        for i,j in zip(a,b):
            x.append(i+j)
        return x

    '''
    Return subtraction of two vectors
    '''
    def sub(self, a, b):
        x = []
        for i,j in zip(a,b):
            x.append(i-j)
        return x