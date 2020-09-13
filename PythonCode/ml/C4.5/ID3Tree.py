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
'''


'''
需要用到的包
'''
import math
import pandas as pd
import numpy as np
import operator


data = pd.read_csv(r'决策树-银行贷款.csv')
data.drop(columns=['ID'], inplace=True)
dataSet = data.values
labels = list(data.columns)


'''
计算熵
输入:数据集
输出:熵
'''
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * math.log2(prob)
    return shannonEnt


#print(calcShannonEnt(dataSet))

'''
用不同特征划分数据集
输入:
    dataSet    数据集
    axis       dataSet中的第几列
    value      划分的值(划分标准)
输出:以某个特征值划分得到的数据集(出去本次划分的特征列)
'''
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            retDataSet.append(np.delete(featVec, axis))     #除去本特征
    return np.array(retDataSet)

    
#z = pd.DataFrame(splitDataSet(dataSet, 0, '青年'))


'''
求最大信息增益的特征列
输入:数据集
输出:信息增益最大特征列的索引
'''
def chooseBestFeatureTosplit(dataSet):
    numFeatures = len(dataSet[0]) - 1           #特征个数
    baseEntropy = calcShannonEnt(dataSet)       #总熵
    bestInfoGain = 0.0                          #初始化信息增益
    bestFeature = -1                            #初始化信息增益最大的列索引
    for i in range(numFeatures):                #循环的是 特征
        featList = [example[i] for example in dataSet]      
        uniqueVals = set(featList)              #计算各个特征中   类别个数
        newEntropy = 0.0
        for value in uniqueVals:                #循环的是 特征中的 类别
            subDataSet = splitDataSet(dataSet, i, value)        #按特征划分数据集
            prob = len(subDataSet) / float(len(dataSet))        #计算 特征中 某个类型占所有的 比值
            newEntropy += prob * calcShannonEnt(subDataSet)     #在某个特征的划分下，新数据集的 总熵
        infoGain = baseEntropy - newEntropy                     #计算每种划分方式的熵(每个特征的信息增益)
        print(infoGain)
        if infoGain > bestInfoGain:             #计算最大的信息增益，并返回
            bestInfoGain = infoGain
            bestFeature = i
    print(bestFeature)
    return bestFeature
    
#print(chooseBestFeatureTosplit(dataSet))


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


print(createTree(dataSet, labels))

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
    
    testLabel = np.array([])
    for testVec in testMatrix:
        classLabel = classify(inputTree, featLabels, testVec)
        testLabel = np.append(testLabel, classLabel)
    return testLabel.reshape(-1,1)
    


#data = pd.read_csv(r'tree_test.csv')
#data.drop(columns=['ID'], inplace=True)
#labels1 = list(data.columns)
#labels2 = list(data.columns)
#dataSet = data.values
# 
#myTree = createTree(dataSet, labels1)
#print(myTree)
#pred = classifyMa(myTree, labels2, test)
#print(pred)
