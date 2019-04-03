from collections import defaultdict
import os
import re
import jieba
import codecs
import xlrd
import numpy as np
import cut as cut
"""
 打开excel格式文件
"""
filename = "C:\\Users\\hasee\\Desktop\\信息管理课程设计\\小米8京东商品评论2.xlsx"
f = open(filename,'r',encoding='utf-8',errors='ignore')
data=xlrd.open_workbook(filename)
table = data.sheet_by_name("Sheet1")
comments=[0 for i in range(5100)]
cut_comments=[0 for i in range(5100)]
comment_time=table.col_values(colx=4,start_rowx=1,end_rowx=None) #获取所有评论对应的时间
print(comment_time)
#获取评论数据
for i in  range(0,5100):
    comments[i]=table.cell_value(rowx=i,colx=3)
#对文本数据进行切分
swfile = open("stop_words.txt",encoding='utf-8')
for i in range(0,5100):
    cut_comments[i]=cut.sent2word(comments[i])
    print(cut_comments[i])


def sent2word(comment):
    """
    Segment a sentence to words
    Delete stopwords
    """
    swfile = open("stop_words.txt")
    segList = jieba.lcut(comment)
    segResult = []
    for w in segList:
        segResult.append(w)

    stopwords = swfile.readLines()
    newSent = []
    for word in segResult:
        if word in stopwords:
            # print "stopword: %s" % word
            continue
        else:
            newSent.append(word)

    return newSent


"""
2. 情感定位
"""


def classifyWords(wordDict):
    # (1) 情感词
    senList = readLines('BosonNLP_sentiment_score.txt')
    senDict = defaultdict()
    for s in senList:
        senDict[s.split(' ')[0]] = s.split(' ')[1]
    # (2) 否定词
    notList = readLines('notDict.txt')
    # (3) 程度副词
    degreeList = readLines('degreeDict.txt')
    degreeDict = defaultdict()
    for d in degreeList:
        degreeDict[d.split(',')[0]] = d.split(',')[1]

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for word in wordDict.keys():
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[wordDict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    return senWord, notWord, degreeWord


"""
3. 情感聚合
"""


def scoreSent(senWord, notWord, degreeWord, segResult):
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    senloc = -1
    # notloc = -1
    # degreeloc = -1

    # 遍历句中所有单词segResult，i为单词绝对位置
    for i in range(0, len(segResult)):
        # 如果该词为情感词
        if i in senLoc:
            # loc为情感词位置列表的序号
            senloc += 1
            # 直接添加该情感词分数
            score += W * float(senWord[i])
            # print "score = %f" % score
            if senloc < len(senLoc) - 1:
                # 判断该情感词与下一情感词之间是否有否定词或程度副词
                # j为绝对位置
                for j in range(senLoc[senloc], senLoc[senloc + 1]):
                    # 如果有否定词
                    if j in notLoc:
                        W *= -1
                    # 如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])
        # i定位至下一个情感词
        if senloc < len(senLoc) - 1:
            i = senLoc[senloc + 1]
    return score