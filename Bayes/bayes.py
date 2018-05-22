# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 16:12:55 2015

@author: Administrator
"""

from numpy import *

# 创建实验样本，可能需要对真实样本做一些处理，如去除标点符号
def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1] # 1代表存在侮辱性的文字，0代表不存在
    return postingList, classVec

# 将所有文档所有词都存到一个列表中，用set()函数去除重复出现的词
def createVocabList(dataSet):
    vocabSet = set([])
    for doc in dataSet:
        vocabSet = vocabSet | set(doc) # 两集合的并集
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList) # 创建和vocabList一样长度的全0列表
    for word in inputSet:
        if word in vocabList: # 针对某段words进行处理
            returnVec[vocabList.index(word)] = 1 # ?
        else:
            print "The word :%s is not in the vocabulary!" % word
    return returnVec

def trainNaiveBayes(trainMatrix, classLabel):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pBase = sum(classLabel) / float(numTrainDocs)
    # The following Settings aim at avoiding the probability of 0
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if classLabel[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p0 = log(p0Num / p0Denom)
    p1 = log(p1Num / p1Denom)
    return p0, p1, pBase

# test the algorithm
def naiveBayesClassify(vec2Classify, p0, p1, pBase):
    p0res = sum(vec2Classify * p0) + log(1 - pBase)
    p1res = sum(vec2Classify * p1) + log(pBase)
    if p1res > p0res:
        return 1
    else:
        return 0

def testNaiveBayes():
    loadData, classLabel = loadDataSet()
    vocList = createNonRepeatedList(loadData)
    trainMat = []
    for doc in loadData:
         trainMat.append(detectInput(vocList, doc))
    p0, p1, pBase = trainNaiveBayes(array(trainMat), array(classLabel))
    testInput = ['love', 'my', 'dalmation']
    thisDoc = array(detectInput(vocList, testInput))
    print testInput, 'the classified as: ', naiveBayesClassify(thisDoc, p0, p1, pBase)
    testInput = ['stupid', 'garbage']
    thisDoc = array(detectInput(vocList, testInput))
    print testInput, 'the classified as: ', naiveBayesClassify(thisDoc, p0, p1, pBase)

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p0Vect = p0Num / p0Denom
    p1Vect = p1Num / p1Denom
    return p0Vect, p1Vect, pAbusive

if __name__ == '__main__':
    listOPosts,listClasses = loadDataSet()
    myVocabList=createVocabList(listOPosts)
    print setOfWords2Vec(myVocabList, listOPosts[0])
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    print trainMat
    p0v,p1v,pAb = trainNB0(trainMat, listClasses)
    print pAb
    print p0v
    print p1v
