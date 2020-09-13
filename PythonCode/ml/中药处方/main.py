# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 10:55:49 2019

@author: admin
"""

import numpy as np
import pandas as pd
import random

def step1():
    zdcp=originData[0:,-1:]
    zdcp = np.unique(zdcp)
    zdcp_cf_repeat={}
    zdcp_cf_norepeat={}
    #键值是列表，后期存储药
    for i in zdcp:
        zdcp_cf_repeat[i]=[]
        zdcp_cf_norepeat[i]=[]      
    for i in zdcp:
        for r in range(originData.shape[0]):        
            if originData[r][-1]==i:
                for j in originData[r][-3].split(','):
                    zdcp_cf_repeat[i].append(j)
                    zdcp_cf_norepeat[i].append(j)
        zdcp_cf_norepeat[i]=list(set(zdcp_cf_norepeat[i]))
        while '' in zdcp_cf_norepeat[i]:
            zdcp_cf_norepeat[i].remove('')
        while '' in zdcp_cf_repeat[i]:
            zdcp_cf_repeat[i].remove('')
    return zdcp_cf_repeat,zdcp_cf_norepeat

def step4(zdcp_cf_repeat,zdcp_cf_norepeat):
    relationFileName='关联分析/调理-肝脾不调关联分析.csv'
    relationFile=pd.read_csv(relationFileName,header=None,encoding = 'gbk')
    relationFile=relationFile.iloc[1:,:].values
    supList=[]
    for i in range(relationFile.shape[0]):
        supList.append(relationFile[i][-2])
    #随机选支持度大于0.38的两味药    
    unionList=[]
    medicines=[]
    while 1:
        randomSup=random.randint(0,len(supList)-1)
        if float(supList[randomSup])>0.38:
            break
        else:
            continue
    for i in eval(relationFile[randomSup][-1]):
        unionList.append(i)
    while i in zdcp_cf_norepeat['IVFET调理-肝脾不调']:
        
    #循环加药
    print(zdcp_cf_norepeat)        
    

if __name__=='__main__':
    dataPath='原始数据1csv.csv'
    originData=pd.read_csv(dataPath,header=None,encoding = 'gbk')
    originData=originData.iloc[1:,:].values
    
    zdcp_cf_repeat,zdcp_cf_norepeat=step1()
#    diseaseName='调理-肝脾不调'
    relationFile=step4(zdcp_cf_repeat,zdcp_cf_norepeat)