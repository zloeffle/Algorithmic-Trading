import pandas as pd
import numpy as np
import math

'''
Implementation of the K-Nearest Neighbors Classifier
'''
class KNN:
    def __init__(self,k):
        self.k = k

    # Calculates distance between two vectors
    def eulicidean_distance(self,v1,v2):
        dist = 0
        v1 = np.array(v1)
        v2 = np.array(v2)

        for i,j in zip(v1,v2):
            dist += (i-j) ** 2

        return math.sqrt(dist)

    # get the k closest neighbors to the test data point
    def get_neightbors(self,train,test):
        dist = []
        tickers = list(train.index)
        
        for t in tickers:
            temp = self.eulicidean_distance(test,train.loc[t,:])
            dist.append((t,temp,train.loc[t,'7-Day Profit']))
        
        dist.sort(key=lambda x: x[1])
        return dist[:self.k]

    # Returns the most frequent label from a points neighbors
    def classify(self,neighbors):
        labels = {}
        
        for n in neighbors:
            if n[2] not in labels:
                labels[n[2]] = 1
            else:
                labels[n[2]] += 1

        most_freq = max(labels,key=labels.get)
        return most_freq
    

        