# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:17:07 2019

@author: admin
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib

data=pd.read_csv("MachineLearning/Part 3 - Classification/Section 10 - Logistic Regression/Social_Network_Ads.csv")
#x=data.iloc[:,1:4].values
x=data.iloc[:,1:4].values
y=data.iloc[:,-1].values

labelcode_x=LabelEncoder()
x[:,0]=labelcode_x.fit_transform(x[:,0])
oneoht=OneHotEncoder(categorical_features=[0])
x=oneoht.fit_transform(x).toarray()
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

#ss=StandardScaler()
#xtrain=ss.fit_transform(xtrain)
#xtest=ss.fit_transform(xtest)

logistic=LogisticRegression(random_state=0)
logistic.fit(xtrain,ytrain)

ypred=logistic.predict(xtest)
res=confusion_matrix(ytest,ypred)

joblib.dump(logistic, "logistic_model.txt")
print("正确率：",(res[0][0]+res[1][1])/res.sum())