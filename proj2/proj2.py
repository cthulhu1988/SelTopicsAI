#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #2
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import re
import operator
from timeit import default_timer as timer
import time
from datetime import timedelta

def main():
    # Hardcoded file handles
    trainData = "train.txt"
    testData = "test.txt"
    # this opens the training and testing files and saves the sentence objects
    # in a list of sentence objects for further use. There is also a boolean in canse it is testing data
    listOfTrainSentenceObjs = openTXTFile(trainData, False)
    listOfTestingSentenceObjs = openTXTFile(testData, True)

    # This is the total count of unique words in the training corpus.
    global getTotalWordCount
    getTotalWordCount = CountWords(listOfTrainSentenceObjs)

    #### Get a total of some specific word ####
    #print(getTotalCount.WordCount("."))
    # create ngrams for the testing data set.
    trainNgramCount = Ngrams(listOfTrainSentenceObjs)

    # passing in testing sentences and NGRAMS created during training.
    runThroughData(listOfTestingSentenceObjs, trainNgramCount)


    outputDataToConsole(getTotalWordCount, trainNgramCount)

########################### CLASSES ###########################
def runThroughData(TestObjs, trainNgramCount):
    biCounter = [0,0,0,0,0]
    triCounter = [0,0,0,0,0]
    for single in TestObjs:
        # iterate through each sentence,
        biCounter[4]+=1
        #print("Line from Testing set: ",single.line)
        #tupl = (single.w_1, single.targetWord)
        #trigramtupl = (single.w_2, single.w_1, single.targetWord)
        #print("target word in Testing sentence: {}".format(single.targetWord))
        #sorted_dict = {}
        newDict = { key:value for (key,value) in trainNgramCount.bigramDict.items() if key[0] == single.w_1}
        test_list = []

        for key, value in newDict.items():
            percentage = value/getTotalWordCount.WordCount(single.targetWord)
            new_tuple = (key[0],key[1])
            #sorted_dict[new_tuple] = percentage
            test_tuple = (key[0],key[1], percentage)
            test_list.append(test_tuple)
        test_list.sort(key=operator.itemgetter(2), reverse=True)
        test_list = test_list[0:10] if len(test_list) >=10 else test_list[0:len(test_list)]

        for idx, item in enumerate(test_list):
            tupleTarget, guess, percentage = item
            #print("{}  {} {}   {}".format(idx,tupleTarget, guess, percentage))
            if guess == single.targetWord:
                if idx == 0:
                    biCounter[0]+=1
                elif idx <= 3:
                    biCounter[1]+=1
                elif idx <= 5:
                    biCounter[2]+=1
                elif idx <= 10:
                    biCounter[3]+=1
        print(biCounter)

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

## Class for dealing with the trigrams. Takes in a sentence object and performs operations on it.
class Ngrams():
    def __init__(self, SentObj):
        self.SentObjList = SentObj
        self.bigramDict = {} ; self.trigramDict = {}
        self.bigramList = [] ; self.trigramList = []
        # split the list into bigrams and trigrams
        for item in self.SentObjList:
            self.bigramList.append(self.splitIntoBigram(item.returnSentence()))
            self.trigramList.append(self.splitIntoTrigram(item.returnSentence()))
        self.dictionaryCount(self.bigramList, self.bigramDict)
        self.dictionaryCount(self.trigramList, self.trigramDict)
        # number of bigrams and trigrams in each dictionary.
        self.bigramNum = len(self.bigramDict)
        self.trigramNum = len(self.trigramDict)

    def dictionaryCount(self, list, dict):
        for item in list:
            for i in item:
                dict[i] = dict.get(i,0) + 1
    # super complicated functions for creating bigrams and trigrams
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

# this class returns different data based on whether or not the bool is set. If testing
# then we need to strip off the last integer to know what word to focus on .
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
    # generaic print stats function I put in a lot of my classes to make sure the program
    # is manipulating data correctly.
    def printStats(self):
        print(self.targetWord)
        print(self.num)
        print(self.sentence)
        print()
    def returnSentence(self):
        return self.sentence


########################### FUNCTIONS ###########################
def outputDataToConsole(getTotalWordCount, trainNgramCount):
    print("Unique unigrams extracted: {}".format(getTotalWordCount.count))
    print("Unique bigrams extracted: {}".format(trainNgramCount.bigramNum))
    print("Unique trigrams extracted: {}".format(trainNgramCount.trigramNum))


def openTXTFile(file, bool):
    SentObj = []
    with open(file, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        words = line.split()
        if len(words) > 0:
            new_obj = Sentence(words, bool)
            SentObj.append(new_obj)
        # pattern = "[0-9a-zA-Z]"
        # words = [word for word in line_list if re.search(pattern,word)]
        while line:
            line = fp.readline()
            words = line.split()
            if len(words) > 0:
                new_obj = Sentence(words, bool)
                SentObj.append(new_obj)
    return SentObj

if __name__ == '__main__':
    main()
