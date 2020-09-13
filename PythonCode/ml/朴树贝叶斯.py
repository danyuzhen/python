# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 12:25:48 2019

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:46:33 2019

@author: admin
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 13:17:07 2019

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
from matplotlib.colors import ListedColormap
from sklearn.naive_bayes import GaussianNB

data=pd.read_csv("MachineLearning/Part 3 - Classification/Section 10 - Logistic Regression/Social_Network_Ads.csv")
x=data.iloc[:,2:4].values
y=data.iloc[:,-1].values

xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

ss=StandardScaler()
xtrain=ss.fit_transform(xtrain)
xtest=ss.fit_transform(xtest)

logistic=LogisticRegression(random_state=0)
logistic.fit(xtrain,ytrain)

svm=SVC(kernel='rbf',random_state=0)
svm.fit(xtrain,ytrain)

bayes=f=GaussianNB()
bayes.fit(xtrain,ytrain)

svm_ypred=svm.predict(xtest)
ypred=logistic.predict(xtest)
ypred_bayes=bayes.predict(xtest)

print(confusion_matrix(ytest,ypred))
print(confusion_matrix(ytest,svm_ypred))
print(confusion_matrix(ytest,ypred_bayes))
