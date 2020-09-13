# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:57:33 2019

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
data=pd.read_csv("test1\\data.csv")
#--------------------
x=data.iloc[:,:-1].values
y=data.iloc[:,-1].values
# #--------------------分类数据（可选,包含虚拟编码）---------------------
labelcode_x=LabelEncoder()
labelcode_y=LabelEncoder()
###########指数拆分#################
x8_lv=[]
for i in x[:,8]:
    num=1/int(i.replace("S",""))
    x8_lv.append( '%.2f' % num )
x[:,8]=x8_lv
##########虚拟编码#################
x[:,3]=labelcode_x.fit_transform(x[:,3])
oneoht=OneHotEncoder(categorical_features=[3])
x=oneoht.fit_transform(x).toarray()
#--------------------拆分训练集数据集---------------------
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)
#------------------多项回归--------------------
polyREG=PolynomialFeatures(degree=4)
xpoly=polyREG.fit_transform(x)
##########线性回归###################
linREG2=LinearRegression()
linREG2.fit(xpoly,y)
#-----------------验证
ypred=linREG2.predict(polyREG.fit_transform(xtest))
x_plt=[]
ypred_float=[]
miss=[]

# for i in ypred:
    # ypred_float.append( float('%.3f' % i ))
# ypred_float=np.array(ypred_float)  
  
# for i in range(len(xtest)):
    # x_plt.append(i+1)  

# for i in range(len(ypred_float)):
    # miss.append(abs(float(ypred_float[i]-ytest[i])))
    
# plt.scatter(x_plt,ytest,color="red")
# plt.scatter(x_plt,ypred_float,color="blue")

# print(ypred_float)
# print(ytest)
# print(miss)
