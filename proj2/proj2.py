#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #2
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import csv
import random
import numpy as np
import re

def main():
    testData = "test.txt"
    listOfSentenceObjs = openTXTFile(testData)
    bigramCount = Bigrams(listOfSentenceObjs)


########################### CLASSES ###########################

class Bigrams():
    def __init__(self, SentObj):
        self.SentObjList = SentObj
        for item in self.SentObjList:
            print(item.returnSentence())


    def splitIntoBigram(self):
        res = [(x, i.split()[j + 1]) for i in test_list for j, x in enumerate(i.split()) if j < len(i.split()) - 1]

class Sentence():
    def __init__(self, line):
        self.line = line
        self.start = "<s>"; self.end = "</s>"
        self.num = int(self.line[-1])
        self.sentence = self.line[:-1]
        self.targetWord = self.sentence[self.num]
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
def openTXTFile(file):
    SentObj = []
    with open(file, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        line_list = line.split()
        pattern = "[0-9a-zA-Z]"
        words = [word for word in line_list if re.search(pattern,word)]
        new_obj = Sentence(words)
        SentObj.append(new_obj)
        while line:
            line = fp.readline()
            words = line.split()
            #pattern = "[0-9a-zA-Z]"
            #words = [word for word in line_list]
            if len(words) > 0:
                new_obj = Sentence(words)
                SentObj.append(new_obj)
    return SentObj

if __name__ == '__main__':
    main()
