#!/usr/bin/env python3
#Isaac G Callison
# CSCI 6350-001
#Project #1
#Due: 01/30/20 

import csv
import random

def main():
    # hardcoded files to be imported
    leviDistance = "costs.csv"; confDistance = "costs2.csv"; wordList = "words.txt"

    # object with 2d array wherein matices and word lists reside.
    leviObj = matrixObj(openCSVFile(leviDistance)); confObj = matrixObj(openCSVFile(confDistance))
    wordObjList = (openTXTFile(wordList))

    for item in wordObjList:
        item.printList()



######################### CLASSES ##########################

class matrixObj:
    def __init__(self, array):
        self.array = array

    def printMatrix(self):
        for row in self.array:
            print(row)

class WordObj:
    def __init__(self, list):
        self.targetWord = list[0]
        self.sourceList = list[1:]
    def printList(self):
        print("Target word is {}".format(self.targetWord))
        print("Source Words are: ")
        for word in self.sourceList:
            print(word, end=" ")
        print()


##################### Manage Words and CSV files ###########################
def openTXTFile(file):
    listWordObjs = []
    f = open(file)
    for row in f:
        row = row.split()
        listWordObjs.append(WordObj(row))
    return listWordObjs

def openCSVFile(file):
    a = []
    with open(file, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter =' ')
        for row in reader:
            r = []
            [r.append(item) for item in row]
            a.append(r)
    return a


if __name__ == '__main__':
    main()
