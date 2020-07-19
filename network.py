import pandas as pd
import numpy as np
import random
import math

class Neural_Network:
    def __init__(self,inputs,targets):
        self.inputs = inputs # inputs for the mlp model
        self.targets = targets # target values
        
        self.input_size = len(self.inputs[0]) # size of each input
        self.num_inputs = len(inputs) # total number of inputs
        
        self.weights = [random.random() for _ in range(self.input_size + 1)] # initialize weights randomly
        self.bias = 0.3
        self.learning_rate = 0.05

    def sigmoid(self,x):
        return 1/(1 + np.exp(-x))
    
    def sigmoid_derivative(self,x):
        return self.sigmoid(x) * (1-self.sigmoid(x))
    
    def mean_square_error(self,target,output):
        return 0.5 * math.pow((target-output),2)
    
    def gradient_descent(self):
        pass
    
    def train(self):
        prev_weights = self.weights
        new_weights = []

        #while prev_weights != new_weights:
        for i in range(100):
            prev_weights = new_weights

            # for each training example and its label
            for i in range(self.num_inputs):
                y = self.predict(self.inputs[i])
                e = self.mean_square_error(self.targets[i],y)
                print(e)
                
                # if error is 0 continue, otherwise update weights
                if e == 0:
                    continue
                elif e > 0:
                    self.weights = self.add(self.weights,self.inputs[i])
                else:
                    self.weights = self.sub(self.weights,self.inputs[i])
                    
                new_weights = self.weights
        return self.weights
        
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