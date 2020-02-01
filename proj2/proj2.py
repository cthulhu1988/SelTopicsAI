#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #1
#Due: 2/6/20
# Please see answers to questions at the bottom of this code.
import csv
import random
import numpy as np
import re

def main():
    testData = "test.txt"
    r = openTXTFile(testData)
    for obj in r:
        obj.printStats()


########################### CLASSES ###########################

class Sentence():
    def __init__(self, line):
        self.line = line
        self.sentence = self.line[:-1]
        self.num = self.line[-1]
    def printStats(self):
        print(self.line)
        print("INDEX", self.num)



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
            line_list = line.split()
            pattern = "[0-9a-zA-Z]"
            words = [word for word in line_list if re.search(pattern,word)]
            if len(words) > 0:
                new_obj = Sentence(words)
                SentObj.append(new_obj)
    return SentObj

if __name__ == '__main__':
    main()
