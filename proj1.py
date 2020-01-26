#!/usr/bin/env python3
#Isaac G Callison
# CSCI 6350-001
#Project #1
#Due: 01/30/20

import csv
import random
import numpy as np

def main():
    # hardcoded files to be imported
    leviDistance = "costs.csv"; confDistance = "costs2.csv"; wordList = "words.txt"

    # object with 2d array wherein matices and word lists reside.
    leviObj = matrixObj(openCSVFile(leviDistance)); confObj = matrixObj(openCSVFile(confDistance))
    wordObjList = (openTXTFile(wordList))
    #leviObj.printMatrix()

    item1 = wordObjList[0]
    n,m = item1.getSrcLeng(0), item1.getTrgtLeng()
    # n is leng of source X string and m in leng of Target Y string
    print("Source {} and target {}".format(item1.sourceList[0], item1.targetWord))
    print("n {} and m {}".format(n,m))
    # source is the siderow X , target is the top Y_row
    scrMatInit = scoreMatrixInit(n,m)
    print(scrMatInit)



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
    def getTrgtLeng(self):
        return len(self.targetWord)
    def getSrcLeng(self, num=0):
        return len(self.sourceList[num])
    def printList(self):
        print("Target word is {}".format(self.targetWord))
        print("Source Words are: ")
        for word in self.sourceList:
            print(word, end=" ")
        print()


##################### Manage Words and CSV files ###########################
def scoreMatrixInit(n,m):
    n,m = n+1,m+1
    i,j = n,m
    score_matrix = np.zeros((n, m), dtype=int)
    for i in range(1,n):
        score_matrix[i,0] = score_matrix[i-1,0] + 1
    for j in range(1,m):
        score_matrix[0,j] = score_matrix[0, j-1] + 1
    return score_matrix

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

def print_matrix(score_matrix, top_seq_col, left_seq_row):
    leng = len(left_seq_row)
    print("    G A A T T C A G T T A")
    for i in range(score_matrix.shape[0]):
        if i == 0:
            print("  ", end="")
        else:
            print(left_seq_row[i-1], end=" ")
        for j in range(score_matrix.shape[1]):
            num = score_matrix[i,j]
            if num < 0:
                print(score_matrix[i,j],end='')
            else:
                print(score_matrix[i,j],end=' ')
        print()
    print()

if __name__ == '__main__':
    main()
