# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:38:18 2019

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import statsmodels.formula.api as sm
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC

data=pd.read_csv("spark_csv.csv")
x=data.iloc[:,:-1].values
y=data.iloc[:,-1].values

labelcode_x=LabelEncoder()
x[:,0]=labelcode_x.fit_transform(x[:,0])
oneoht=OneHotEncoder(categorical_features=[0])
x=oneoht.fit_transform(x).toarray()
#x=x[:,1:]
ss=StandardScaler()
x=ss.fit_transform(x)

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

svm=SVC(kernel='rbf',random_state=0)
svm.fit(xtrain,ytrain)

svm_ypred=svm.predict(xtest)

res=confusion_matrix(ytest,svm_ypred)
print("错误率：",(res[0][1]+res[1][0])/res.sum())
