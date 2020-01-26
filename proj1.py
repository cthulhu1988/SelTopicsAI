#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
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

    item1 = wordObjList[0]
    n,m = item1.getSrcLeng(0), item1.getTrgtLeng()
    # n is leng of source X string and m in leng of Target Y string
    # source is the siderow X , target is the top Y_row
    # GET BACK intialized matrix.
    scrMatInit = scoreMatrixInit(n,m)

    print(scrMatInit)
    # FINISH filling up the score matix. Change based on levinstein or confusion
    scrMatrix = fillScoreMatrix(n,m,scrMatInit)

    print(scrMatrix)


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
def fillScoreMatrix(n,m,scoreMat):
    n,m = n+1,m+1
    i,j = n,m
    for i in range(1,n):
        for j in range(1,m):
            scoreMat[i][j] = return_min(scoreMat, i, j)
    return scoreMat

def return_min(matrix, i, j):
    add = 0
    gap_penalty = 1
    # diag = (matrix[j-1,i-1] + add)
    # left = (matrix[j,i-1] + gap_penalty)
    # up = (matrix[j-1,i] + gap_penalty)
    #
    # min_val = min(diag,left,up)
    # return min_val
    return 1

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


if __name__ == '__main__':
    main()
