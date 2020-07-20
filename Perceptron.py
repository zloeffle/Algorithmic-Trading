import pandas as pd
import numpy as np
import random

'''
Implementation of a multilayer perceptron network
'''
class MLP:
    def __init__(self,inputs,targets):
        self.inputs = inputs # inputs for the mlp model
        self.targets = targets # target values
        
        self.input_size = len(self.inputs[0]) # size of each input
        self.num_inputs = len(inputs) # total number of inputs
        
        self.weights = [random.random() for _ in range(self.input_size + 1)] # initialize weights randomly
    
    '''
    Threshold activation function
    Returns the activation value
    '''
    def activation(self,n):
        if n >= 0:
            return 1
        return 0
        
    '''
    Implementation of the perceptron learning algorithm
    '''
    def train(self):
        prev_weights = self.weights
        new_weights = []
        
        # iterate until weights do not change
        while prev_weights != new_weights:
        #for i in range(1000):
            prev_weights = new_weights
            # for each training example and its label
            for i in range(self.num_inputs):
                y = self.predict(self.inputs[i])
                e = self.targets[i] - y
                
                # if error is 0 continue, otherwise update weights
                if e == 0:
                    continue
                elif e > 0:
                    self.weights = self.add(self.weights,self.inputs[i])
                else:
                    self.weights = self.sub(self.weights,self.inputs[i])
                    
                new_weights = self.weights
        return self.weights
    
    '''
    Returns a prediction based on input values
    '''
    def predict(self,inputs):
        z = self.dot(self.weights,inputs)
        a = self.activation(z)
        print('W*X: %f  Activation: %d' % (z,a))
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

if __name__ == '__main__':
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = [0, 1, 1, 1]
    pcn = MLP(inputs, targets)

    '''# OR gate
    pcn.train()
    outputs = [pcn.predict(p) for p in inputs]
    print(outputs, targets)
    assert outputs == targets'''

    # AND gate
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = [0, 0, 0, 1]

    pcn = MLP(inputs, targets)
    pcn.train()
    outputs = [pcn.predict(p) for p in inputs]
    print(outputs, targets)
    assert outputs == targets

    print('ALL TESTS PASSED')