# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:04:39 2019

@author: admin
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import impute
from sklearn.preprocessing import LabelEncoder,OneHotEncoder,PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
import statsmodels.formula.api as sm
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from matplotlib.colors import ListedColormap

data=pd.read_csv("svm实验课\\data.csv")
#    data=data.replace('?',np.nan)
data=data.replace('+',1)
data=data.replace('-',0)
x=data.iloc[:,:-1].values
y=data.iloc[:,-1].values
pd.set_option('display.max_columns',None)

#-----------------------删除“？”行
list_a=[]
for i in range(x.shape[0]):
    for j in range(x.shape[1]):
        if x[i][j]=="?":
            list_a.append(i)
list_a = list(set(list_a))
x = np.delete(x, list_a, axis=0)
y = np.delete(y, list_a, axis=0)
labelcode_x=LabelEncoder()

x[:,0]=labelcode_x.fit_transform(x[:,0])
x[:,3]=labelcode_x.fit_transform(x[:,3])
x[:,4]=labelcode_x.fit_transform(x[:,4])
x[:,5]=labelcode_x.fit_transform(x[:,5])
x[:,6]=labelcode_x.fit_transform(x[:,6])
x[:,8]=labelcode_x.fit_transform(x[:,8])
x[:,9]=labelcode_x.fit_transform(x[:,9])
x[:,11]=labelcode_x.fit_transform(x[:,11])
x[:,12]=labelcode_x.fit_transform(x[:,12])


#x[:,3]=labelcode_x.fit_transform(x[:,3])
#oneoht=OneHotEncoder(categorical_features=[3])


#x[:,4]=labelcode_x.fit_transform(x[:,4])
#x[:,5]=labelcode_x.fit_transform(x[:,5])
#x[:,6]=labelcode_x.fit_transform(x[:,6])
#x[:,8]=labelcode_x.fit_transform(x[:,8])
#x[:,9]=labelcode_x.fit_transform(x[:,9])
#x[:,11]=labelcode_x.fit_transform(x[:,11])
#x[:,12]=labelcode_x.fit_transform(x[:,12])

#oneoht=OneHotEncoder(categorical_features=[3])  
#oneoht=OneHotEncoder(categorical_features=[4]) 
#oneoht=OneHotEncoder(categorical_features=[5]) 
#oneoht=OneHotEncoder(categorical_features=[6]) 
#oneoht=OneHotEncoder(categorical_features=[8]) 
#oneoht=OneHotEncoder(categorical_features=[9]) 
#oneoht=OneHotEncoder(categorical_features=[11]) 
#oneoht=OneHotEncoder(categorical_features=[12]) 

#---------------------降维
#ss=StandardScaler()
#x=ss.fit_transform(x)
##--------------------训练----------------------
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

svm=SVC(kernel='rbf',random_state=0)
svm.fit(xtrain,ytrain)

svm_ypred=svm.predict(xtest)
res=confusion_matrix(ytest,svm_ypred)
print("错误率：",(res[0][1]+res[1][0])/res.sum())














#--------------------缺失数据---------------------
imputer=impute.SimpleImputer(missing_values=np.nan,strategy="most_frequent")
imputer_mean=impute.SimpleImputer(missing_values=np.nan,strategy="mean")
x[:,[0,3,4,5,6,8,9,11,12]]=imputer.fit_transform(x[:,[0,3,4,5,6,8,9,11,12]])
x[:,[1,2,7,10,13,14]]=imputer_mean.fit_transform(x[:,[1,2,7,10,13,14]])
 #--------------------分类数据（可选）---------------------
labelcode_x=LabelEncoder()

x[:,0]=labelcode_x.fit_transform(x[:,0])
x[:,3]=labelcode_x.fit_transform(x[:,3])
x[:,4]=labelcode_x.fit_transform(x[:,4])
x[:,5]=labelcode_x.fit_transform(x[:,5])
x[:,6]=labelcode_x.fit_transform(x[:,6])
x[:,8]=labelcode_x.fit_transform(x[:,8])
x[:,9]=labelcode_x.fit_transform(x[:,9])
x[:,11]=labelcode_x.fit_transform(x[:,11])
x[:,12]=labelcode_x.fit_transform(x[:,12])

#oneoht=OneHotEncoder(categorical_features=[0])     
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[4])  
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[7]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[10]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[24]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[34]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[36]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[39]) 
#x=oneoht.fit_transform(x).toarray()
#oneoht=OneHotEncoder(categorical_features=[41]) 
#x=oneoht.fit_transform(x).toarray()

#--------------------特征缩放--------------------
ss=StandardScaler()
x=ss.fit_transform(x)
#--------------------训练----------------------
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=0)

svm=SVC(kernel='rbf',random_state=0)
svm.fit(xtrain,ytrain)

svm_ypred=svm.predict(xtest)
res=confusion_matrix(ytest,svm_ypred)
print("错误率：",(res[0][1]+res[1][0])/res.sum())
