#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #2
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import re
import random
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
    triCounter = [0,0,0,0,0]

    # create ngrams for the testing data set.
    trainNgramCount = Ngrams(listOfTrainSentenceObjs)

    # passing in testing sentences and NGRAMS created during training.
    triCounter = trigramCalc(testData, trainNgramCount, triCounter)
    # output final data to the screen
    outputDataToConsole(getTotalWordCount, trainNgramCount, triCounter)
###############################################################
########################### CLASSES ###########################
###############################################################
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
    # Increments count to each unique word in the word dictionary
    def gWCnt(self, sentence):
        for item in sentence:
            sent = item.returnSentence()
            for i in sent:
                self.wordDict[i] = self.wordDict.get(i,0) + 1
        self.count = len(self.wordDict)

## Class for dealing with the bigrams/trigrams. Takes in a sentence object and performs operations on it.
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
    #determine number of each unique bigram and trigram
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
    # Splits the sentece into a trigram tuple and appends.
    def splitIntoTrigram(self, test_list):
        leng = len(test_list)
        tupl = []
        for x in range(2,leng):
            tup = (test_list[x-2], test_list[x-1], test_list[x])
            tupl.append(tup)
        return tupl

# This class returns different data based on whether or not the bool is set. If testing
# then we need to strip off the last integer to know what word to focus on .
class Sentence():
    def __init__(self, line, testing=False):
        self.targetWord = ""
        self.num = -1
        self.line = line
        self.start = "<s>"; self.end = "</s>"
        ## If testing is true we need to extract more information from the setence.
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
    # Generic print stats function I put in a lot of my classes to make sure the program
    # is manipulating data correctly.
    def printStats(self):
        print(self.targetWord)
        print(self.num)
        print(self.sentence)
        print()
        # just returns a bigram sentence.
    def returnSentence(self):
        return self.sentence
        # this returns a sentence for use with trigrams Extra padding.
    def returnTriSentence(self):
        triSetence = self.sentence
        triSetence.insert(0,self.start)
        triSetence.append(self.end)
        return triSetence

#################################################################
########################### FUNCTIONS ###########################
#################################################################
# This function parses each incoming testing sentence, filters the bigram and trigram dictionaries based on the
# target word and previous one or two words, performs matches, and increments a counter array. I am rather fond
# of that counter array, saves space when counting multiple variables.
def trigramCalc(data, trainNgramCount, triCounter):
    # I spent a great deal of time trying to reduce the processing time in this section. Best run is 5 mins 41 secs on a I7-4790K
    t_dict = trainNgramCount.trigramDict.items()
    b_dict = trainNgramCount.bigramDict.items()
    start = "<s><s>"; end = "</s></s>"
    triCounter = [0,0,0,0,0]
    # this encoding allowed me to pull in the sentences without error.
    with open(data, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        while line:
            triCounter[4]+=1
            words = line.split()
            if len(words) > 0:
                # perform operations on the strings:
                num = int(words[-1])
                #num = random.randrange(0,len(words)-1)
                sentence = words[:-1]
                targetWord = sentence[num]
                # setting the words previous to the target word.
                w_1 = sentence[num-1] if len(words) >=1 else ""
                w_2 = sentence[num-2] if len(words) >=2 else ""
                sentence.insert(0,start)
                sentence.append(end)
                # create dictionaries and lists:
                # Turn dictionary into list, sort by highest, cut of list at 10, set a bool to avoid double counting:
                found_match = False
                trigramDict = {k:v for (k,v) in t_dict if (k[0] == w_2 and k[1] == w_1)  }
                trigram_list = []
                # convert filtered dictionary into a list and sort.
                for key, value in trigramDict.items():
                    trigram_list.append((key[0],key[1],key[2], value))
                    trigram_list.sort(key=operator.itemgetter(3), reverse=True)
                # We only need a slice of the top 10
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

                # if we did not find a match in the previous trigram section we try bigrams.
                # The program ran faster if I checked trigrams first, then bigrams if there was no match.
                # create dictionaries and lists:
                # Turn dictionary into list, sort by highest, cut off list at 10, check with a bool to avoid double counting:
                if found_match == False:
                    bigram_list = []
                    bigramDict = {k:v for (k,v) in b_dict if (k[0] == w_1)  }
                    for key, value in bigramDict.items():
                        bigram_list.append((key[0],key[1], value))
                        bigram_list.sort(key=operator.itemgetter(2), reverse=True)
                    # We only need a slice of the top 10
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
# The purpose of this function is to output the final data to the console.
def outputDataToConsole(getTotalWordCount, trainNgramCount, triCounter):
    print("Unique unigrams extracted: {}".format(getTotalWordCount.count))
    print("Unique bigrams extracted: {}".format(trainNgramCount.bigramNum))
    print("Unique trigrams extracted: {}".format(trainNgramCount.trigramNum))
    outputSentence(1, triCounter[0], triCounter[4])
    outputSentence(3, triCounter[1], triCounter[4])
    outputSentence(5, triCounter[2], triCounter[4])
    outputSentence(10, triCounter[3], triCounter[4])

# This function proves that there is no task so trivial that I won't wrap it into a function or class.
# Behold my cleverly named variables.
def outputSentence(a,b,c):
    print("# of times correct word found in top {} highest probability n-grams {} of {} predictions".format(a,b,c))

# responsible for opening files, splitting sentences and creating sentence objects for the sentence class above.
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

ANSWER: Well, in my testing the top 1 results were 667 out of 4332 predictions. That is a relatively low percentage (about 15%) of correct answers.
However, this is also a very simplistic way to approach the problem. Not that the implementation was easy, just that the criterion for selecting
a word is error prone. Just because a word has a higher percentage of following another does not mean it is likely or will occur every time. This is
not a problem that would be resolved with a larger corpus necessarily. It may show improvement if the testing and training corpora had similar stilted
formulaic speech patters. Still, the results are not trivial in their significance. This n-gram selection process works remarkably well for such a
naive implementation.

2. The test sentences are extracted randomly from the news stories used in the training data. A sentence is in
either the training data or the test data, but not both. Discuss the pros and cons of this approach.

ANSWER: With regard to pros, it is a better real world test of how accurate the language model is for predicting answers from data that
the model has not encountered before. With regard to cons, the accuracy will be lower when dealing with data the model has not seen.
I was able to run the training data back through as if it were testing data by randomly selecting a target word to predict. Obviously not something
that we would normally do. However, the accuracy increased to 52% in top 1 and 81% in top 10 predictions out of the 17226 lines in the training data.

3. What, in your opinion, is a better way to split the data into training and test components? Give reasons for
your answer.

ANSWER: From previous exposure to testing and training data, I think the proper process in this case would be to randomize the sentences,
take a larger slice as training data, then take the small remaining slice as testing data. This randomization ensures there is no bias
in the training data. I believe it may also protect against underfitting and overfitting.


"""
