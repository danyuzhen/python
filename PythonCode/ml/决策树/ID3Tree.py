'''
Created on 2019年5月15日

@author: Tree

使用python语言实现决策树中的ID3算法.
要求:
1.按要求补全下面缺失的代码.
2.不用实现剪枝和树的可视化.
3.本次实验的输入、输出、代码内部的数据处理和计算 都用ndarray(numpy).(在本实验中，所有函数输入的数据集，默认最后一列为"标签")
4.写代码的时候可以用"银行贷款数据"，最后测试用蘑菇分类数据集.
5.这次实验以个人为单位，每人交一份自己写的代码，星期五晚班长统一发我.(备注好 姓名、班级、学号)
6.参考资料"机器学习实战.pdf"，第三章决策树.
'''

'''
需要用到的包
'''
import math
import pandas as pd
import numpy as np
import operator
from math import log
import operator

'''
计算熵
输入:数据集
输出:熵
'''
def calcShannonEnt(dataSet):
    data_len=len(data)
    label={}
    entroy=0.0
    #每个结果的数量
    for i in range(data.shape[0]):
#        result_type=data[data.shape[1]-1][i]
        result_type=data[i,-1]
        if result_type not in label.keys():
            label[result_type]=0
        label[result_type]+=1
    #计算熵
    for label_key in label:
        prob=float(label[label_key])/data_len
        entroy-=prob*log(prob,2)
    return entroy


'''
用不同特征划分数据集
输入:
    dataSet    数据集
    axis       dataSet中的第几列
    value      划分的值(划分标准)
输出:以某个特征值划分得到的数据集(出去本次划分的特征列)
'''
def splitDataSet(dataset, axis, value):
    retdataset=[]
    for i in range(dataset.shape[0]):
        if dataset[i,axis]==value:  
            retdataset.append(dataset[i,axis+1:].tolist())
    return retdataset
    

'''
求最大信息增益的特征列
输入:数据集
输出:信息增益最大特征列的索引
'''
def chooseBestFeatureTosplit(dataSet):
    dataSet=dataSet[:,1:]
    numFeatures = len(dataSet[0])              
    baseEntropy = calcShannonEnt(dataSet)                 
    bestInfoGain = 0.0
    bestFeature = -1
    newEntroy = 0.0
    featList=[]
    #列数
    for i in range(numFeatures):
        
        #得出所有特征（每列的值去重）
        #featList = [example[i] for example in dataSet]
        for example in dataSet:
            featList.append(example[i])
        uniqueVals = set(featList)
        
        #每一列的信息增益
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prop = len(subDataSet)/float(len(dataSet))
            newEntroy += prop * calcShannonEnt(subDataSet)  #计算条件信息熵
        infoGain = baseEntropy-newEntroy                   #信息增益
        
        #找出信息增益大于0的那列
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i    
    return bestFeature,uniqueVals
    

'''
表决器
输入:类别标签组成的一个list
输出:某一个类别
'''
def majorityCnt(classList):
    classCount = {}
    for i in range(classList[:,1:].shape[0]):
        for j in range(classList[:,1:].shape[1]):
            if classList[:,1:][i,j] not in classCount.keys():
                classCount[classList[:,1:][i,j]]=0
            else:
                classCount[classList[:,1:][i,j]]+=1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
    
    
'''
创建树
输入:
    dataSet:数据集
    labels:特征名称组成的list
输出:保存树信息的嵌套字典(因为是递归进行，所有是嵌套字典)
'''
def createTree(dataSet, labels):
#    dataSet=dataSet[:,1:]
    #结果列
    classlist = [example[-1] for example in dataSet]
    
    #如果只有一个特征
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    #如果数据集中的特征已用完，将剩下样本中出现次数最大的标签，作为剩下所有样本的标签
    if dataSet[0][0] == 1:
        return majorityCnt[classlist]
    
    #选择熵值变化最大的特征
    bestFeat= chooseBestFeatureTosplit(dataSet)
    bestFeat=bestFeat[0]
    #取得对应特征的标签
    bestFeatLabel = labels[bestFeat]
    #构造对应特征的字典
    myTree = {bestFeatLabel:{}}
#    #将对应的标签从标签数组中删除
    labels = labels[:]
    del(labels[bestFeat])
#    #取得对应特征的所有取值
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


'''
使用决策树 预测
输入:
    inputTree:保存树信息的字典
    featLabels:特征名称组成的list
    testVec:要预测的数据(单条、list)
输出:类别标签
'''
def classify(inputTree, featLabels, testVec):
    firstStr  = inputTree.keys()[0]
    secondDict = inputTree[firstStr]

    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel


'''
使用决策树 预测，输入为 矩阵
输入:
    inputTree:保存树信息的字典
    featLabels:特征名称组成的list
    testMatrix:多条需要预测数据组成的ndarray
输出:多个类别标签组成的ndarray
'''
def classifyMa(inputTree, featLabels, testMatrix):
    
    pass

    return testLabel.reshape(-1,1)
    
if __name__!='__mian__':
    data=pd.read_csv('决策树-银行贷款.csv',header=None)
    data=data.iloc[1:,:].values
    entroy=calcShannonEnt(data)
    retdataset=splitDataSet(data,1,'老年')
    bestFeature,uniqueVals=chooseBestFeatureTosplit(data)
    sortedClassCount=majorityCnt(data)
    myTree=createTree(data,list(uniqueVals))
    classLabel=classify(myTree, list(uniqueVals), data[1,:])