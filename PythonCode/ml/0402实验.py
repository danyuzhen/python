# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:56:25 2019

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

train_data=pd.read_csv("泰坦尼克/train.csv",header=None)
test_data=pd.read_csv("泰坦尼克/test.csv",header=None)

x=train_data.iloc[1:,[2,5,6,7,9]].values
y=train_data.iloc[1:,1].values
#xtest=test_data.iloc[1:,[1,4,5,6,8]].values

imputer=Imputer(missing_values="NaN",strategy="mean",axis=0)
imputer=imputer.fit(x)
x=imputer.transform(x)
#imputer=imputer.fit(xtest)
#xtest=imputer.transform(xtest)



xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

logistic=LogisticRegression(random_state=0)
logistic.fit(xtrain,ytrain)

ypred=logistic.predict(xtest)
cm=confusion_matrix(ytest,ypred)

a=0
for i in range(len(ypred)):
    if ypred[i]==ytest[i]:
        continue
    else:
        a=a+1
print(a/len(ytest))
