# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 18:59:13 2019

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
import sys
import random
import csv

data=pd.read_csv("Data.csv")
country=data.iloc[:,0:1].values
age=data.iloc[:,1:2].values
salary=data.iloc[:,2:3].values
Purchased=data.iloc[:,3:4].values

age_list=[]
country_list=[]
salary_list=[]
purchased_list=[]
for i in range(600):
    age_list.append(random.randint(20,60))
    salary_list.append(random.randint(40000,100000))
    if random.randint(1,3)==1:
        country_list.append(country[0][0])
    if random.randint(1,3)==2:
        country_list.append(country[1][0])
    if random.randint(1,3)==3:
        country_list.append(country[2][0])
    
    if random.randint(1,2)==1:
        purchased_list.append(0)
    if random.randint(1,2)==2:
        purchased_list.append(1)
for i in range(500):
    line=[]
    line=[country_list[i],age_list[i],salary_list[i],purchased_list[i]]    
    f=csv.writer(open("spark_csv.csv","a",newline=""),dialect='excel')
    f.writerow(line)
    print(line)     