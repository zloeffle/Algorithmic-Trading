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
            print('%s[%s < %.3f] Gini = %.4f' % (depth*' ',node.feat, node.thresh, node.gini))
            self.print(node.left, depth+1)
            self.print(node.right, depth+1)
        else:
            print('%s[%s]' % (depth*' ',node))

    def partition(self,data,feature,value):
        true_df,false_df = {},{}
        rows = list(data.index)
        
        for row in rows:
            if data.loc[row,feature] <= value:
                true_df[row] = list(data.loc[row,:].values)
            else:
                false_df[row] = list(data.loc[row,:].values)
                
        true_df = pd.DataFrame.from_dict(true_df,orient='index',columns=data.columns)
        false_df = pd.DataFrame.from_dict(false_df,orient='index',columns=data.columns)
        return true_df,false_df
        
    def gini_index(self,groups):
        gini = 0.0
        instances = float(sum([len(group) for group in groups]))
        
        for group in groups:
            n = float(len(group))
            if n == 0:
                continue

            t = sum(group['7-Day Profit'] == 1)/n
            f = sum(group['7-Day Profit'] == 0)/n
            gini += (1-(math.pow(t,2) + math.pow(f,2))) * (n/instances)

        gini = round(gini,4)
        #print(gini)
        return gini
        
    # returns node that results in the optimal split
    def best_split(self,data):
        best_feature,best_threshold,best_gini,best_groups = None,math.inf,math.inf,None
        cols = list(data.columns)
        tickers = list(data.index)

        for column in cols[:-1]:
            for row in tickers:
                groups = self.partition(data,column,data.loc[row,column])
                gini = self.gini_index(groups)
                
                if gini < best_gini:
                    best_feature = column
                    best_threshold = data.loc[row,column]
                    best_gini = gini
                    best_groups = groups

        node = Node()
        node.feat = best_feature
        node.thresh = best_threshold
        node.gini = best_gini
        node.left,node.right = best_groups
        node.print()
        return node
    
    # make a node terminal
    def terminal(self,group):
        vals = group['7-Day Profit']
        t = sum(vals == 1)
        f = sum(vals == 0)
        if t >= f:
            return True
        else:
            return False

    # generate left and right children for a node or make it terminal
    def split(self,node,depth,min_size):
        left,right = node.left,node.right

        # check for no split
        if left is None or right is None:
            node.left,node.right = self.terminal(left+right)
            return node

        # check for max depth
        if depth >= self.max_depth:
            node.left = self.terminal(left)
            node.right = self.terminal(right)
            return node

        # process left child
        if len(left) <= min_size:
            node.left = self.terminal(left)
        else:
            node.left = self.best_split(left)
            self.split(node.left, depth+1,min_size)

        # process right child
        if len(right) <= min_size:
            node.right = self.terminal(right)
        else:
            node.right = self.best_split(right)
            self.split(node.right, depth+1,min_size)

    # build the decision tree
    def build_tree(self,data,min_size):
        root = self.best_split(data)
        self.split(root,10,1)
        return root
    
    # predict based on a row of data
    def predict(self):
        pass
    