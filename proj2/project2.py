#!/usr/bin/env python
# coding: utf-8

def generate_ngrams(filename, n):
    grams = {}
    tokens=[]

    if(n!=1):
        terminate = n-1
    else:
        terminate = 0

    with open(filename) as fp:
        line = fp.readline()

        while line:
            value = 0
            line = line.rstrip()
            if(n == 1 or n==2):
                line = '<s> '+line + ' </s>'
            if(n == 3):
                line = '<s> <s> '+line + ' </s> </s>'
            s = line.split(" ")
            tokens = (s)
            for i in range(len(tokens)-terminate):
                if(n==1):
                    key = tokens[i]
                elif(n==2 and i+1 < len(tokens)):
                    key = tokens[i] + " " + tokens[i+1]
                elif(n==3 and  i+2 < len(tokens)):
                    key = tokens[i] + " " + tokens[i+1] + " " + tokens[i+2]

                if key in grams:
                    value = grams[key] + 1
                else:
                    value = 1
                grams[key] = value
            line = fp.readline()
    return grams


def getTrigramPredictDict (listTokens, trigrams, cntPredictTrigrams):
    index = int(listTokens[-1])
    predictTriStr = listTokens[index-2] + ' ' + listTokens[index-1] + ' ' + listTokens[index]
    key, value = trigrams[0]
    if(predictTriStr == key):
        cntPredictTrigrams = cntPredictTrigrams+1


def getBigramPredictDict (listTokens, bigrams, cnt1Bi):
    new_dict = {}
    index = int(listTokens[-1])
    predictBiStr = listTokens[index-1] + ' ' + listTokens[index]
    #print('---'+predictBiStr)
    str = predictBiStr.split(" ")
    target_word = str[1]
    prev_word = str[0]

    for i in range(len(bigrams)):
        key,value = bigrams[i]
        dict_str = key.split(" ")
        dict_target = dict_str[1]
        dict_prev = dict_str[0]
        if(target_word == dict_target):
            new_dict[key] = value

    for i,(k,v) in enumerate(new_dict.items()):
        if(i==1 and k== predictBiStr):
            cnt1Bi  = cnt1Bi+1
        if i== 10:
            break;

    print(new_dict)
    return cnt1Bi

"""def getBigramPredictDict (listTokens, bigrams, cntPredictBigrams):
    index = int(listTokens[-1])
    predictBiStr = listTokens[index-1] + ' ' + listTokens[index]
    if(predictBiStr in bigrams):
        temp = list(bigrams.items())
        res = [idx for idx, key in enumerate(temp) if key[0] == predictBiStr]
        if(res[0] < 800):
            cntPredictBigrams = cntPredictBigrams+1
    return cntPredictBigrams
"""

def computeCount (tokens, sortedBigrams, sortedTrigrams, cntPredictBigram, globalBiDictTen, globalTriDictTen):
    probabilityDict = {}
    index = int(listTokens[-1])
    target_word = tokens[index]
    target_bigram = listTokens[index-1] + ' ' + listTokens[index]
    target_trigram = listTokens[index-2] + ' ' + listTokens[index-1] + ' ' + listTokens[index]
    cntPredictBigram = getBigramPredictDict(tokens, sortedBigrams, cntPredictBigram, globalBiDictTen)
    bigramProb = -1
    trigramProb = -1
    if(target_word in globalBiDictTen):
        topTenBiFrequency = globalBiDictTen[target_word]
        if(target_bigram in topTenBiFrequency):
            bigramProb = topTenBiFrequency[target_bigram]

    if(target_word in globalTriDictTen):
        topTenTriFrequency = globalTriDictTen[target_word]
        if(target_trigram in topTenTriFrequency):
            trigramProb = topTenTriFrequency[target_trigram]



def read_test_file(filename, sortedBigrams, sortedTrigrams):
    cntPredictBigram = 0
    cntPredictTrigram = 0
    globalBiDictTen = {}

    #print(sortedBigrams)
    with open(filename) as fp:
        line = fp.readline()
        while line:
            line = line.rstrip()
            tokens = line.split(" ")
            computeCount(tokens, sortedBigrams, cntPredictBigram, globalBiDictTen)
            #getTrigramPredictDict(tokens, sortedTrigrams, cntPredictTrigram)
            line = fp.readline()
    print(cntPredictBigram)
    #print(cntPredictTrigram)


trainFile = 'train.txt'
testFile = 'test.txt'

unigrams = generate_ngrams(trainFile,1)
print('Unique unigrams extracted: %s'%len(unigrams))

bigrams = generate_ngrams(trainFile,2)
#print(bigrams)
print('Unique bigrams extracted: %s'%len(bigrams))

trigrams = generate_ngrams(trainFile, 3)
print('Unique trigrams extracted: %s'%len(trigrams))
#print(trigrams)



sortedBigrams = sorted(bigrams.items(), key=lambda item: item[1], reverse=True)
#sortedBigrams = {k: v for k, v in sorted(bigrams.items(), key=lambda item: item[1])}
sortedTrigrams = sorted(trigrams.items(), key=lambda item: item[1], reverse=True)
read_test_file(testFile, sortedBigrams, sortedTrigrams)
