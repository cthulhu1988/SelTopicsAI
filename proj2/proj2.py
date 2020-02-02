#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #2
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import re

def main():
    # Hardcoded file handles
    trainData = "train.txt"
    testData = "test.txt"
    # this opens the training and testing files and saves the sentence objects
    # in a list of sentence objects for further use.
    listOfTrainSentenceObjs = openTXTFile(trainData, False)
    listOfTestingSentenceObjs = openTXTFile(testData, True)

    # This is the total count of unique words in the training corpus.
    getTotalCount = CountWords(listOfTrainSentenceObjs)
    total = getTotalCount.count
    # print("total uniq {}".format(total))

    #print(getTotalCount.WordCount("."))
    trainNgramCount = Ngrams(listOfTrainSentenceObjs)
    # print(trainNgramCount.trigramNum)


    single = listOfTestingSentenceObjs[1]
    print(single.targetWord)
    print(single.w_1)
    print(single.w_2)
    tupl = (single.w_1, single.targetWord)

    for key, value in trainNgramCount.bigramDict.items():
        if key == tupl:
            print("Key: {}   Num times: {}".format(key, value))

########################### CLASSES ###########################

class CountWords():
    def __init__(self, SentObj):
        self.SentObj = SentObj
        self.wordDict = {}
        self.gWCnt(self.SentObj)

    def WordCount(self,word):
        for k,v in self.wordDict.items():
            if k == word:
                return v

    def gWCnt(self, sentence):
        for item in sentence:
            sent = item.returnSentence()
            for i in sent:
                self.wordDict[i] = self.wordDict.get(i,0) + 1
        self.count = len(self.wordDict)


class Ngrams():
    def __init__(self, SentObj):
        self.SentObjList = SentObj
        self.bigramDict = {} ; self.trigramDict = {}
        self.bigramList = []
        self.trigramList = []
        for item in self.SentObjList:
            self.bigramList.append(self.splitIntoBigram(item.returnSentence()))
            self.trigramList.append(self.splitIntoTrigram(item.returnSentence()))
        self.dictionaryCount(self.bigramList, self.bigramDict)
        self.dictionaryCount(self.trigramList, self.trigramDict)
        self.bigramNum = len(self.bigramDict)
        self.trigramNum = len(self.trigramDict)

    def dictionaryCount(self, list, dict):
        for item in list:
            for i in item:
                dict[i] = dict.get(i,0) + 1

    def splitIntoBigram(self, test_list):
        leng = len(test_list)
        tupl = []
        for x in range(1,leng):
            tup = (test_list[x-1], test_list[x])
            tupl.append(tup)
        return tupl

    def splitIntoTrigram(self, test_list):
        leng = len(test_list)
        tupl = []
        for x in range(2,leng):
            tup = (test_list[x-2], test_list[x-1], test_list[x])
            tupl.append(tup)
        return tupl


class Sentence():
    def __init__(self, line, testing=False):
        self.targetWord = ""
        self.num = -1
        self.line = line
        self.start = "<s>"; self.end = "</s>"
        ## If testing is true
        if testing == True:
            self.num = int(self.line[-1])
            self.sentence = self.line[:-1]
            self.targetWord = self.sentence[self.num]
            self.w_1 = self.sentence[self.num-1] if self.num >=1 else ""
            self.w_2 = self.sentence[self.num-2] if self.num >=2 else ""
        # else we are training and there is no number at the end.
        elif testing == False:
            self.sentence = self.line

        self.sentence.insert(0,self.start)
        self.sentence.append(self.end)

    def printStats(self):
        print(self.targetWord)
        print(self.num)
        print(self.sentence)
        print()
    def returnSentence(self):
        return self.sentence




########################### FUNCTIONS ###########################
def openTXTFile(file, bool):
    SentObj = []
    with open(file, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        words = line.split()
        if len(words) > 0:
            new_obj = Sentence(words, bool)
            SentObj.append(new_obj)
        # line = fp.readline()
        # line_list = line.split()
        # pattern = "[0-9a-zA-Z]"
        # words = [word for word in line_list if re.search(pattern,word)]
        # new_obj = Sentence(words)
        # SentObj.append(new_obj)
        while line:
            line = fp.readline()
            words = line.split()
            #pattern = "[0-9a-zA-Z]"
            #words = [word for word in line_list]
            if len(words) > 0:
                new_obj = Sentence(words, bool)
                SentObj.append(new_obj)
    return SentObj

if __name__ == '__main__':
    main()
