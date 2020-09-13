'''
Created on 2019年5月22日

@author: Tree

Tree C4.5
使用python语言实现决策树中的C4.5算法.
要求:
1.按要求补全下面缺失的代码.
2.不用实现剪枝和树的可视化.
3.本次实验的输入、输出、代码内部的数据处理和计算 都用ndarray(numpy).(在本实验中，所有函数输入的数据集，默认最后一列为"标签")
4.写代码的时候可以用"银行贷款数据"，最后测试用蘑菇分类数据集.
5.这次实验以个人为单位，每人交一份自己写的代码，星期五晚班长统一发我.(备注好 姓名、班级、学号)
'''

'''
需要用到的包
'''
import math
import pandas as pd
import numpy as np
import operator
from math import log
import sys
'''
计算熵
输入:数据集
输出:熵
'''
def calcShannonEnt(data):
    #data行数
    data_len=len(data)
    label={}
    entroy=0.0
    #每个结果的数量
    for i in data[:,-1]:
        if i not in label.keys():
            label[i]=1
        else:
            label[i]+=1
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
    for i in dataset:
        if i[axis]==value:  
            retdataset.append(list(i[axis+1:]))
    return np.array(retdataset)

'''
求最大信息增益"率"的特征列
输入:数据集
输出:信息增益率最大特征列的索引
'''
def chooseBestFeatureTosplit(dataset):

    numFeatures = len(dataset[0]) - 1           #特征个数,除去最后一列
    baseEntropy = calcShannonEnt(dataset)       #总熵
    ratio_list=[]                              
    for i in range(numFeatures):
        #每列的值                
        featList = [example[i] for example in dataset]   
        #每列的值去重，得出特征
        uniqueVals = set(featList)              
        newEntropy = 0.0
        #循环每个特征
        for value in uniqueVals:
            #每个特征与每列传入，以某个特征值划分得到的结果
            subDataSet = splitDataSet(dataset, i, value)     
            #划分后的行数占总数的百分比
            prob = len(subDataSet) / float(len(dataset)) 
            #新数据集的总熵
            newEntropy += prob * calcShannonEnt(subDataSet)
         #每个特征的信息增益   
        infoGain = baseEntropy - newEntropy   
        #信息增益率
        ratio_list.append(infoGain/newEntropy)
    return ratio_list.index(max(ratio_list))
    

'''
表决器
输入:类别标签组成的一个list
输出:某一个类别
'''
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]
    
    
'''
创建树
输入:
    dataSet:数据集
    labels:特征名称组成的list
输出:保存树信息的嵌套字典(因为是递归进行，所有是嵌套字典)
'''
def createTree(dataSet, labels):        #labels特征名称
    classList = [example[-1] for example in dataSet]        #取每次循环的最后一个值，将其组成list

    if classList.count(classList[0]) == len(classList):     #类别完全相同  停止划分
        return classList[0]             #最终字典的 值
    if len(dataSet[0]) == 1:            #遍历完所有特征
        return majorityCnt(classList)   #最终字典的 值
    bestFeat = chooseBestFeatureTosplit(dataSet)            #计算信息增益最大的特征
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}             #存储树的所有信息
    del(labels[bestFeat])                   #删除本次遍历   信息增益最大的特征名称
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValues = set(featValues)          #得到本次遍历   信息增益最大特征的  所有值
    for value in uniqueValues:              #for循环加递归 构建树的每一个分支
        subLabels = labels[:]               #剩下所有特征的名称
        dict_value = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)      
        myTree[bestFeatLabel][value] = dict_value         #向字典中保存信息
    
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
    firstStr = list(inputTree.keys())[0]            #取最外层 字典键
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)          #返回键在 标签中的索引位置
    for key in secondDict.keys():                   #循环  key
        if testVec[featIndex] == key:               #此特征项   和  哪一个键 相等
            if type(secondDict[key]).__name__ == 'dict':        #查看是否为 叶节点
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

'''特征列表'''
def data_label(data):
     #特征个数,除去最后一列
    numFeatures = len(data[0]) - 1
    label=[]                        
    for i in range(numFeatures):
        #每列的值                
        featList = [example[i] for example in data]   
        #每列的值去重，得出特征
        uniqueVals = set(featList) 
        for j in uniqueVals:
            label.append(j) 
    return label

if __name__!='__mian__':
    data=pd.read_csv('决策树-银行贷款.csv',header=None)
    data=data.iloc[1:,1:].values
    data_label=data_label(data)
    
    entroy=calcShannonEnt(data)
    ratio_index_max=chooseBestFeatureTosplit(data)
    myTree=createTree(data,data_label)