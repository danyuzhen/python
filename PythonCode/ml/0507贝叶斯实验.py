# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 23:30:12 2019

@author: admin
"""
import numpy as np
import pandas as pd
from sklearn import impute
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB

data=pd.read_csv("0507bayes_csv\\data.csv",encoding="gbk")
data=data.replace('？',np.nan)
data=data.replace('NaN',np.nan)
data=data.replace('nan',np.nan)
data=data.replace('',np.nan)
pd.set_option('display.max_columns',None)
x=data.iloc[:,1:-1].values
y=data.iloc[:,-1].values

#--------------------缺失数据---------------------
imputer=impute.SimpleImputer(missing_values=np.NaN,strategy="mean")
x[:,:]=imputer.fit_transform(x[:,:])
x[379,-1]=abs(x[379,-1])
x=x.astype(float)
#--------每行0列数量
zero_list=[]
for i in range(x.shape[0]):
    zero=0
    for  j in list(x[i]):
        if j==0.0:
            zero=zero+1
    if zero>4:
        zero_list.append(i)

#--------删除0元素在4列以上的行        
x = np.delete(x, zero_list, axis=0)
y = np.delete(y, zero_list, axis=0)

#--------------------特征缩放--------------------
#ss=StandardScaler()
#x=ss.fit_transform(x)
#--------------------训练----------------------
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)
bayes=f=GaussianNB()
bayes.fit(xtrain,ytrain)

ypred_bayes=bayes.predict(xtest)
res=confusion_matrix(ytest,ypred_bayes)

print("正确率：",(res[0][0]+res[1][1])/res.sum())
