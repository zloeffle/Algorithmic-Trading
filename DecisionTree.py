import pandas as pd
import numpy as np
import math
from sklearn.model_selection import train_test_split

'''
Class representation of a node in the decision tree
'''
class Node:
    def __init__(self):
        self.left = None # left child
        self.right = None # right child
        self.feat = None # feature node represents
        self.thresh = 0 # threshold value for node
        self.gini = 0 # split cost

    # print visual representation of a node
    def print(self):
        print('Feature:',self.feat)
        print('Threshold:',self.thresh)
        print('Cost:',self.gini)
        print('Left:\n',self.left)
        print('Right:\n',self.right)
        

'''
Class representation of a decision tree model
'''
class DecisionTree:
    def __init__(self, max_depth=5):
        self.max_depth = max_depth # maximum depth of the tree

    # print a visual representation of the tree
    def print(self,node,depth=0):
        if isinstance(node,Node):
            print('%s[%s < %.3f] Gini = %.4f' % (depth*' ',node.feat, node.thresh, node.gini))
            self.print(node.left, depth+1)
            self.print(node.right, depth+1)
        else:
            print('%s[%s]' % (depth*' ',node))

    '''
    Partitions data into left and right groups based on an attribute and a value for that attribute

    Params: data = input dataframe, feature = feature to get values from, value = value to split data on    
    Returns: tuple(left split dataframe, right split dataframe)
    '''
    def partition(self,data,feature,value):
        left,right = {},{}
        rows = list(data.index)
        
        for row in rows:
            if data.loc[row,feature] <= value:
                left[row] = list(data.loc[row,:].values)
            else:
                right[row] = list(data.loc[row,:].values)
                
        left = pd.DataFrame.from_dict(left,orient='index',columns=data.columns)
        right = pd.DataFrame.from_dict(right,orient='index',columns=data.columns)
        return left,right
         
    '''
    Score used to better understand how mixed the classes are in groups created by a split
    Perfect split gives gini score of 0 while worst case gives split of 0.5 (for 2 class problems)
    
    Params: tuple of groups created by a split
    Returns: float(gini score for the groups)
    '''
    def gini_index(self,groups):
        gini = 0.0
        instances = float(sum([len(group) for group in groups]))
        
        for group in groups:
            n = float(len(group))
            if n == 0:
                continue

            t = sum(group['Kyphosis'] == 1)/n
            f = sum(group['Kyphosis'] == 0)/n
            gini += (1-(math.pow(t,2) + math.pow(f,2))) * (n/instances)

        gini = round(gini,4)
        #print(gini)
        return gini
        
    '''
    Evaluates all possible splits to find the one with the best gini score
    
    Params: dataframe
    Returns: Node() to best split data
    '''
    def best_split(self,data):
        # initialize result values
        best_feature,best_threshold,best_gini,best_groups = None,math.inf,math.inf,None

        # features and rows in dataset
        cols = list(data.columns)
        rows = list(data.index)

        # iterate through features
        for column in cols[:-1]:
            # iterate through each row
            for row in rows:
                # parition data into groups based on each feature and value under that feature
                groups = self.partition(data,column,data.loc[row,column])
                
                # calculate gini score for paritioned data
                gini = self.gini_index(groups)

                # update result values if current score is better than previous score
                if gini < best_gini:
                    best_feature = column
                    best_threshold = data.loc[row,column]
                    best_gini = gini
                    best_groups = groups

        # return node to best split data
        node = Node()
        node.feat = best_feature
        node.thresh = best_threshold
        node.gini = best_gini
        node.left,node.right = best_groups
        return node
    
    '''
    Returns most frequent class to assign to a terminal node
    
    Params: group = dataframe
    Returns: int() most frequent class
    '''
    def terminal(self,group):
        res = {}
        for row in group.index:
            if group.loc[row,'Kyphosis'] not in res:
                res[group.loc[row,'Kyphosis']] = 1
            else:
                res[group.loc[row,'Kyphosis']] += 1
        val = max(res,key=res.get)
        print(group,val)
        return val
    '''
    Build the decision tree through recursive splitting
    
    Params: node = current node to split, depth = current depth, min_size = minimum number of data records a node is responsible for
    Returns: 
    '''
    def split(self,node,depth,min_size):
        left,right = node.left,node.right
       
        # no split if left or right child are None
        if left.empty or right.empty:
            node.left = node.right = self.terminal(left+right)
            return 

        # if max depth is reached set current nodes children to terminal 
        if depth >= 5:
            node.left = self.terminal(left)
            node.right = self.terminal(right)
            return 

        # Process left child
        if len(left) <= min_size: # set as terminal if smaller than min size
            node.left = self.terminal(left)
        else:
            # calculate best split point for left child and recursively split
            node.left = self.best_split(left)
            self.split(node.left,depth+1,min_size)
            
        # process right child
        if len(right) <= min_size:
            node.right = self.terminal(right)
        else:
            # calculate best split point for right child and recursively split
            node.right = self.best_split(right)
            self.split(node.right,depth+1,min_size)

    '''
    Build the decision tree model by calculating the initial best split point and then recursively splitting
    
    Params: data = dataframe, min_size = minimum number of records per node
    Returns: Node() completed tree
    '''
    def build_tree(self,data,min_size):
        root = self.best_split(data)
        self.split(root,0,min_size)
        return root
    
    '''
    Predict the target class for a new row of data
    
    Params: node = current node to split data, data = new data
    Returns: predicted class for test data
    '''
    def predict(self,node,data):
        # check split for new data
        if data[node.feat] < node.thresh:
            # if left child is a Node then move to that node
            if isinstance(node.left,Node):
                return self.predict(node.left,data)
            
            # otherwise return the left childs value
            else:
                return node.left
        else:
            # if right child is a Node then move to that node
            if isinstance(node.right,Node):
                return self.predict(node.right,data)
            # otherwise return the right childs value
            else:
                return node.right

if __name__ == '__main__':
    df = pd.read_csv('data/kyphosis.csv')
    model = DecisionTree(df)
    
    # prepare data
    for row in df.index:
        if df.loc[row,'Kyphosis'] == 'present':
            df.loc[row,'Kyphosis'] = 1
        else:
            df.loc[row,'Kyphosis'] = 0
    
    # split data into training and testing
    x = df.drop('Kyphosis',axis=1)
    y = df['Kyphosis']
    df.drop('Kyphosis',axis=1,inplace=True)
    df['Kyphosis'] = y
    x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.30,random_state=101)
    
    # build tree
    x_train['Kyphosis'] = y_train
    root = model.build_tree(x_train,2)
    
    # predict with new data
    x_train.drop('Kyphosis',axis=1,inplace=True)
    for row in x_train.index:
        pred = model.predict(root,x_train.loc[row,:])
    
    
    