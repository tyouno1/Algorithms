# -*- coding: utf-8 -*-
"""
Created on Tue Sep 08 16:12:55 2015

@author: Administrator
"""

from numpy import *
from pprint import pprint

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
def classifyNB(vec2Classify, p0, p1, pBase):
    p0res = sum(vec2Classify * p0) + log(1 - pBase)
    p1res = sum(vec2Classify * p1) + log(pBase)
    if p1res > p0res:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for doc in listOPosts:
         trainMat.append(setOfWords2Vec(myVocabList, doc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'the classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['help', 'my']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'the classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

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

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2] 

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def spamTest():
    docList=[]; classList = []; fullText =[]
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)#create vocabulary
    trainingSet = range(50); testSet=[]           #create test set
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])  
    trainMat=[]; trainClasses = []
    for docIndex in trainingSet:#train the classifier (get probs) trainNB0
        trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:        #classify the remaining items
        wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            print "classification error",docList[docIndex]
    print 'the error rate is: ',float(errorCount)/len(testSet)
    #return vocabList,fullText

if __name__ == '__main__':
    #listOPosts,listClasses = loadDataSet()
    #pprint(listOPosts)
    #print 'listClasses:', listClasses
    #myVocabList=createVocabList(listOPosts)
    #print 'myVocabList: ' , myVocabList
    #print setOfWords2Vec(myVocabList, listOPosts[0])
    #print setOfWords2Vec(myVocabList, listOPosts[1])
    #print setOfWords2Vec(myVocabList, listOPosts[2])
    #print setOfWords2Vec(myVocabList, listOPosts[3])
    #print setOfWords2Vec(myVocabList, listOPosts[4])
    #print setOfWords2Vec(myVocabList, listOPosts[5])
    #trainMat=[]
    #for postinDoc in listOPosts:
    #    trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    #print 'trainMat:' , trainMat
    #p0v,p1v,pAb = trainNB0(trainMat, listClasses)
    #print 'pAb: ' , pAb
    #print 'p0v: ' , p0v
    #print 'p1v: ' , p1v
    #  ========================================================
    # testingNB()
    #  ========================================================
    spamTest() 
