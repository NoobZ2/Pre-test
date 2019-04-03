import numpy as np
import sys
import re
import codecs
import os
import jieba
from gensim.models import word2vec
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from scipy import stats
from keras.models import Sequentialpi
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from sklearn.metrics import f1_score
from bayes_opt import BayesianOptimization as BO
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

def parseSent(sentence):
    seg_list = jieba.cut(sentence)
    output = ''.join(list(seg_list)) # use space to join them
    return output

def getWordVecs(wordList):
    vecs = []
    for word in wordList:
        word = word.replace('\n', '')
        try:
            vecs.append(model[word])
        except KeyError:
            continue
    # vecs = np.concatenate(vecs)
    return np.array(vecs, dtype = 'float')


def buildVecs(filename):
    posInput = []
    with open(filename, "rb") as txtfile:
        # print txtfile
        for lines in txtfile:
            lines = lines.split('\n ')
            for line in lines:
                line = jieba.cut(line)
                resultList = getWordVecs(line)
                # for each sentence, the mean vector of all its vectors is used to represent this sentence
                if len(resultList) != 0:
                    resultArray = sum(np.array(resultList))/len(resultList)
                    posInput.append(resultArray)

    return posInput

# load word2vec model
model = word2vec.Word2Vec.load_word2vec_format("corpus.model.bin", binary = True)
# txtfile = [u'标准间太差房间还不如3星的而且设施非常陈旧.建议酒店把老的标准间从新改善.', u'在这个西部小城市能住上这样的酒店让我很欣喜，提供的免费接机服务方便了我的出行，地处市中心，购物很方便。早餐比较丰富，服务人员很热情。推荐大家也来试试，我想下次来这里我仍然会住这里']
posInput = buildVecs('pos.txt')
negInput = buildVecs('pos.txt')

# use 1 for positive sentiment, 0 for negative
y = np.concatenate((np.ones(len(posInput)), np.zeros(len(negInput))))

X = posInput[:]
for neg in negInput:
    X.append(neg)
X = np.array(X)