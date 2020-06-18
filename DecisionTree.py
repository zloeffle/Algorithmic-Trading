import numpy as np
import pandas as pd
import math
import random

class Node:
    def __init__(self):
        self.left = None # left child
        self.right = None # right child
        self.is_terminal = False
        self.feat = None # feature node represents
        self.thresh = 0 # threshold value for node
        self.gini = 0 # split cost

    def print(self):
        print('Feature:',self.feat)
        print('Threshold:',self.thresh)
        print('Terminal?:',self.is_terminal)
        print('Cost:',self.gini)
        print('Left:\n',self.left)
        print('Right:\n',self.right)
        

class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth

    # prints a visual representation of the tree
    def print(self,node,depth=0):
        if isinstance(node,Node):
            print('%s[%s < %.3f] Gini = %.4f' % (depth*' ',node.feat, node.thresh, node.cost))
            self.print(node.left, depth+1)
            self.print(node.right, depth+1)
        else:
            print('%s[%s]' % (depth*' ',node))

    def gini_index(self):
        pass
        
    # returns node that results in the optimal split
    def best_split(self,data):
        pass
            
    # make a node terminal
    def terminal(self,node):
        pass

    # generate left and right children for a node or make it terminal
    def split(self):
        pass

    # build the decision tree
    def build_tree(self):
        pass

    # predict based on a row of data
    def predict(self):
        pass
    
if __name__ == '__main__':
    df1 = pd.read_csv('train_04-30-2020.csv')
    df2 = pd.read_csv('train_05-29-2020.csv')
    df3 = pd.read_csv('train_06-01-2020.csv')

    model = DecisionTree()
    df1.set_index('Ticker',inplace=True)
    df2.set_index('Ticker',inplace=True)
    df3.set_index('Ticker',inplace=True)
    print(df1)