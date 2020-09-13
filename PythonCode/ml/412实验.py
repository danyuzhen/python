# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:13:23 2019

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

data=pd.read_csv("csv/data.csv",encoding = "gb2312")



x=data.iloc[:,:-1].values
y=data.iloc[:,-1].values

x0=data.iloc[:,0].values.reshape(len(x),1)
x1=data.iloc[:,1].values.reshape(len(x),1)
x2=data.iloc[:,2].values.reshape(len(x),1)
x3=data.iloc[:,3].values.reshape(len(x),1)
x5=data.iloc[:,5].values.reshape(len(x),1)
x6=data.iloc[:,6].values.reshape(len(x),1)
x8=data.iloc[:,8].values.reshape(len(x),1)
x10=data.iloc[:,10].values.reshape(len(x),1)

###########缺失值
imputer=Imputer(missing_values="NaN",strategy="mean",axis=0)

imputer=imputer.fit( x0.reshape(len(x),1) )
x[:,0]=imputer.transform(x0).reshape(len(x0),)

imputer=imputer.fit( x3.reshape(len(x),1) )
x[:,3]=imputer.transform(x3).reshape(len(x3),)

###########虚拟编码
labelcode_x=LabelEncoder()

x[:,1]=labelcode_x.fit_transform(x[:,1])
#oneoht=OneHotEncoder(categorical_features=[1])

x[:,2]=labelcode_x.fit_transform(x[:,2])
#oneoht=OneHotEncoder(categorical_features=[2])

x[:,5]=labelcode_x.fit_transform(x[:,5])
#oneoht=OneHotEncoder(categorical_features=[5])

x[:,6]=labelcode_x.fit_transform(x[:,6])
#oneoht=OneHotEncoder(categorical_features=[6])

x[:,8]=labelcode_x.fit_transform(x[:,8])
#oneoht=OneHotEncoder(categorical_features=[8])

x[:,10]=labelcode_x.fit_transform(x[:,10])
#oneoht=OneHotEncoder(categorical_features=[10])

#oneoht=OneHotEncoder(categorical_features=[1])
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[3])
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[9])
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[11])
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[15])
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[18])
x=oneoht.fit_transform(x).toarray()

#--------------------特征缩放--------------------
ss=StandardScaler()
x=ss.fit_transform(x)

##############训练
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)


logistic=LogisticRegression(random_state=0)
logistic.fit(xtrain,ytrain)

svm=SVC(kernel='rbf',random_state=0)
svm.fit(xtrain,ytrain)
#
svm_ypred=svm.predict(xtest)
ypred=logistic.predict(xtest)
res_svm=confusion_matrix(ytest,svm_ypred)
res_log=confusion_matrix(ytest,ypred)


print('svm错误率：'+str(res_svm[0][1]+res_svm[1][0]/res_svm.sum()))
print('log错误率：'+str(res_log[0][1]+res_log[1][0]/res_log.sum()))    #逻辑回归

