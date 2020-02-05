#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #2
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import re
import operator
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
    global triCounter
    global biCounter
    biCounter = [0,0,0,0,0]
    triCounter = [0,0,0,0,0]

    # create ngrams for the testing data set.
    trainNgramCount = Ngrams(listOfTrainSentenceObjs)

    # passing in testing sentences and NGRAMS created during training.
    triCounter = trigramCalc(testData, trainNgramCount, triCounter)

    outputDataToConsole(getTotalWordCount, trainNgramCount, triCounter)




########################### CLASSES ###########################

# This class creates a word dictionary from all the setences pulled into the program.
class CountWords():
    def __init__(self, SentObj):
        self.SentObj = SentObj
        self.wordDict = {}
        self.gWCnt(self.SentObj)
    # this method returns the total number of each word in the dictionary.
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
            self.trigramList.append(self.splitIntoTrigram(item.returnTriSentence()))
        # stores number of each type.
        self.dictionaryCount(self.bigramList, self.bigramDict)
        self.dictionaryCount(self.trigramList, self.trigramDict)
        # number of bigrams and trigrams in each dictionary.
        self.bigramNum = len(self.bigramDict)
        self.trigramNum = len(self.trigramDict)

    def dictionaryCount(self, list, dict):
        for item in list:
            for i in item:
                dict[i] = dict.get(i,0) + 1
    # super complicated methods for creating bigrams and trigrams
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
    # generic print stats function I put in a lot of my classes to make sure the program
    # is manipulating data correctly.
    def printStats(self):
        print(self.targetWord)
        print(self.num)
        print(self.sentence)
        print()
    def returnSentence(self):
        return self.sentence
    def returnTriSentence(self):
        triSetence = self.sentence
        triSetence.insert(0,self.start)
        triSetence.append(self.end)
        return triSetence

########################### FUNCTIONS ###########################
def trigramCalc(data, trainNgramCount, triCounter):
    start = "<s>"; end = "</s>"
    triCounter = [0,0,0,0,0]
    with open(data, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        while line:
            triCounter[4]+=1
            words = line.split()
            if len(words) > 0:
                # perform operations on the strings:
                num = int(words[-1])
                sentence = words[:-1]
                targetWord = sentence[num]
                w_1 = sentence[num-1] if num >=1 else ""
                w_2 = sentence[num-2] if num >=2 else ""
                sentence.insert(0,start)
                sentence.append(end)

                # create dictionaries and lists:
                # Turn dictionary into list, sort by highest, cut of list at 10, set a bool to avoid double counting:
                found_match = False
                trigramDict = {k:v for (k,v) in trainNgramCount.trigramDict.items() if (k[0] == w_2 and k[1] == w_1)  }
                trigram_list = []
                for key, value in trigramDict.items():
                    trigram_list.append((key[0],key[1],key[2], value))
                    trigram_list.sort(key=operator.itemgetter(3), reverse=True)

                trigram_list = trigram_list[0:10] if len(trigram_list) >=10 else trigram_list[0:len(trigram_list)]
                for id, y in enumerate(trigram_list):
                    t,tupleTarget, guess, percentage = y
                    if guess == targetWord:
                        found_match = True
                        if id == 0:
                            triCounter[0]+=1
                        if id <= 3:
                            triCounter[1]+=1
                        if id <= 5:
                            triCounter[2]+=1
                        if id <= 10:
                            triCounter[3]+=1


                # create dictionaries and lists:
                # Turn dictionary into list, sort by highest, cut off list at 10, set a bool to avoid double counting:
                # if we did not find a match in the previous trigram section we try bigrams. Best run time is 6 minutes on this.
                if found_match == False:
                    bigram_list = []
                    bigramDict = {k:v for (k,v) in trainNgramCount.bigramDict.items() if (k[0] == w_1)  }
                    for key, value in bigramDict.items():
                        bigram_list.append((key[0],key[1], value))
                        bigram_list.sort(key=operator.itemgetter(2), reverse=True)

                    bigram_list = bigram_list[0:10] if len(bigram_list) >=10 else bigram_list[0:len(bigram_list)]
                    for idx, i in enumerate(bigram_list):
                        tupleTarget, guess, percentage = i
                        if guess == targetWord:
                            if idx == 0:
                                triCounter[0]+=1
                            if idx <= 3:
                                triCounter[1]+=1
                            if idx <= 5:
                                triCounter[2]+=1
                            if idx <= 10:
                                triCounter[3]+=1
                else:
                    pass
            # readline to start process over
            line = fp.readline()
    return triCounter

def outputDataToConsole(getTotalWordCount, trainNgramCount, triCounter):
    print("Unique unigrams extracted: {}".format(getTotalWordCount.count))
    print("Unique bigrams extracted: {}".format(trainNgramCount.bigramNum))
    print("Unique trigrams extracted: {}".format(trainNgramCount.trigramNum))
    outputSentence(1, triCounter[0], triCounter[4])
    outputSentence(3, triCounter[1], triCounter[4])
    outputSentence(5, triCounter[2], triCounter[4])
    outputSentence(10, triCounter[3], triCounter[4])

def outputSentence(a,b,c):
    print("# of times correct word found in top {} highest probability n-grams {} of {} predictions".format(a,b,c))

def openTXTFile(file, bool):
    SentObj = []
    with open(file, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        words = line.split()
        if len(words) > 0:
            new_obj = Sentence(words, bool)
            SentObj.append(new_obj)
        while line:
            line = fp.readline()
            words = line.split()
            if len(words) > 0:
                new_obj = Sentence(words, bool)
                SentObj.append(new_obj)
    return SentObj

if __name__ == '__main__':
    main()

"""
1. Why you believe the results are as output(ed) by your code.
ANSWER:

2. The test sentences are extracted randomly from the news stories used in the training data. A sentence is in
either the training data or the test data, but not both. Discuss the pros and cons of this approach.
ANSWER:

3. What, in your opinion, is a better way to split the data into training and test components? Give reasons for
your answer.
ANSWER:
"""
