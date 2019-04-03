from collections import defaultdict
from math import sqrt

import jieba


def sent2word(sentence):
    """
    1. 文本切割
    """
    """
    Segment a sentence to words
    Delete stopwords
    """

    # sentence = "今天天气挺好的"
    segList = jieba.cut(sentence)
    segResult = []
    for w in segList:
        segResult.append(w)

    stopwords = open('stop_words.txt', 'r', encoding='utf-8').readlines()
    newSent = []
    for word in segResult:
        if word + "\n" in stopwords:
            # print("stopword: %s" % word)
            continue
        else:
            newSent.append(word)

    # print(newSent)
    return newSent


def classifyWords(words_dict):
    """
    2. 情感定位
    """
    # (1) 情感词
    senList = open('BosonNLP_sentiment_score.txt', 'r', encoding='utf-8').readlines()
    senDict = defaultdict()
    for s in senList:
        try:
            senDict[s.split(' ')[0]] = s.split(' ')[1].strip()
        except:
            continue
    # (2) 否定词
    notList = open('notDict.txt', 'r', encoding='utf-8').readlines()
    # (3) 程度副词
    degreeList = open('程度级别词语（中文）.txt', 'r', encoding='utf-8').readlines()
    degreeDict = defaultdict()

    degree = 0.0
    for d in degreeList:
        if "  " in d:
            degree = float(d.split("  ")[1].strip())
            continue
        degreeDict[d] = degree

    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()

    for word in words_dict:
        if word in senDict.keys() and word not in notList and word not in degreeDict.keys():
            senWord[words_dict[word]] = senDict[word]
        elif word in notList and word not in degreeDict.keys():
            notWord[words_dict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[words_dict[word]] = degreeDict[word]

    # print(senWord)
    # print(notWord)
    # print(degreeWord)
    return senWord, notWord, degreeWord


def scoreSent(senWord, notWord, degreeWord, segResult):
    """
    3. 情感聚合
    """
    W = 1
    score = 0
    # 存所有情感词的位置的列表
    senLoc = list(senWord.keys())
    notLoc = list(notWord.keys())
    degreeLoc = list(degreeWord.keys())

    # print(type(list(notLoc)))
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
            # print("score = %f" % score)
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
    # print(score)
    return score


def give_score(sentence):
    words = sent2word(sentence)

    words_dict = {}

    for i, w in enumerate(words):
        words_dict[w] = i

    senWord, notWord, degreeWord = classifyWords(words_dict)

    return scoreSent(senWord, notWord, degreeWord, words)


def comment_sent_analy():
    sentences = open("小米9微博.txt", 'r',encoding='utf-8').readlines()
    res = open("mi9WeiBo.txt", "w", encoding='utf-8')
    for sentence in sentences:
        score = give_score(sentence.strip())/sqrt(sentence.__len__())
        print(sentence.strip())
        print(score)
        res.write(str(sentence.strip())+"\t"+str(score) + "\n")


if __name__ == '__main__':
    comment_sent_analy()
    print()
