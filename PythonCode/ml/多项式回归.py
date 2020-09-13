# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 22:31:01 2019

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
import statsmodels.formula.api as sm

#--------------------导入数据---------------------
data=pd.read_csv("diamonds.csv")
#-------------------
#
x=data.iloc[:,[1,2,3,4,5,6,8,9,10]].values
#x1=data.iloc[:,8:11].values
#x=np.c_[x,x1]
y=data.iloc[:,-4].values

#--------------------分类数据（可选）---------------------
labelcode_x=LabelEncoder()
x[:,1]=labelcode_x.fit_transform(x[:,1])
x[:,2]=labelcode_x.fit_transform(x[:,2])
x[:,3]=labelcode_x.fit_transform(x[:,3])
oneoht=OneHotEncoder(categorical_features=[1])
oneoht=OneHotEncoder(categorical_features=[2])
oneoht=OneHotEncoder(categorical_features=[3])
x=oneoht.fit_transform(x).toarray()
#--------------------拆分训练集数据集---------------------
#xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)
## #-------------多项线性回归--------------------
#polyREG=PolynomialFeatures(degree=3)
#xpoly=polyREG.fit_transform(xtrain)
###########创建多项式回归###################
#linREG2=LinearRegression()
#linREG2.fit(xpoly,ytrain)
## #---------------------画图----------------------
#res=linREG2.predict(polyREG.fit_transform(xtest))-ytest
# print(ytest)
# print(linREG2.predict(polyREG.fit_transform(xtest)))
# print(linREG2.predict(polyREG.fit_transform(xtest))-ytest)
# total=0
# for i in res:
#     total=total+abs(int(i))
# print(total)