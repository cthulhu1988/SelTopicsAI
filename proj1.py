#!/usr/bin/env python3
#Isaac G Callison
#CSCI 6350-001
#Project #1
#Due: 01/30/20

import csv
import math, sys
import random
import numpy as np
from numpy import genfromtxt

def main():
    # hardcoded files to be imported
    leviDistance = "costs.csv"; confDistance = "costs2.csv"; wordList = "words.txt"

    # object with 2d array wherein matices and word lists reside.
    global leviObj
    global confObj
    leviObj = matrixObj(openCSVFile(leviDistance));
    confObj = matrixObj(openCSVFile(confDistance))
    wordObjList = (openTXTFile(wordList))

    item1 = wordObjList[0]
    n,m = item1.getSrcLeng(0), item1.getTrgtLeng()
    # TARGET -> TOP , Y, n, i
    # Source -> SIDE LEFT , X, m, j
    # n/i is leng of source X string and m/j in leng of Target Y string
    # source is the siderow X , target is the top Y_row
    # GET BACK intialized matrix.
    scrMatInit = scoreMatrixInit(n,m)

    #print(scrMatInit)
    # FINISH filling up the score matix. Change based on levinstein or confusion
    targetString = item1.targetWord
    sourceString = item1.sourceList[0]

    scrMatrix, traceback_list, node_list = fillScoreMatrix(n,m,scrMatInit, targetString, sourceString)


    path_list = []
    node_list.reverse()

    node = node_list[0]
    path_obj = pathObj(node.x, node.y)
    path_list.append(path_obj)
    pre_x = node.prev_x ; pre_y = node.prev_y
    for x in range(1,len(node_list)):
        node = node_list[x]
        if node.x == pre_x and node.y == pre_y:
            pre_x = node.prev_x ; pre_y = node.prev_y
            path_obj = pathObj(node.x, node.y)
            path_list.append(path_obj)

    path_obj = pathObj(node.prev_x, node.prev_y)
    path_list.append(path_obj)

    top_seq_col = targetString
    left_seq_row = sourceString

    for item in path_list:
        item.print_stats()

    final_seq1, final_seq2 = traceback(path_list, top_seq_col, left_seq_row)
    final_seq1 = final_seq1[::-1]
    final_seq2 = final_seq2[::-1]
    print(final_seq1)
    print(final_seq2)


    print(scrMatrix)


######################### CLASSES ##########################
class pathObj:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sub_x = None
        self.sub_y = None
    def __sub__(self, obj):
        self.sub_x = (self.x - obj.x)
        self.sub_y = (self.y - obj.y)

    def print_stats(self):
        print("X {} and Y {}".format(self.x, self.y))

    def print_sub(self):
        print("sub X {} and sub Y {}".format(self.sub_x, self.sub_y))

class matrixObj:
    def __init__(self, array):
        self.array = array

    # TARGET -> TOP , Y, n, i ROW
    # Source -> SIDE LEFT , X, m, j
    def printMatrix(self):
        print(np.shape(self.array))
        for row in self.array:
            print(row)
    def getCost(self, i, j):
        return int(self.array[i][j])


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

class TraceObj(object):
    def __init__(self, x, y):
        self.direction_list =[]
        self.x = x
        self.y = y
        self.left = None
        self.up = None
        self.diag = None
        self.previous = None
        self.prev_x = None
        self.prev_y = None

    def set_dir(self):
        if "diag" in self.direction_list:
            self.diag = [self.x-1, self.y-1]
        if "up" in self.direction_list:
            self.up = [self.x, self.y-1]
        if "left" in self.direction_list:
            self.left = [self.x-1, self.y]
        if self.up:
            self.previous = self.up
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
        if self.left:
            self.previous = self.left
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
        if self.diag:
            self.previous = self.diag
            self.prev_x = self.previous[0]
            self.prev_y = self.previous[1]
    def print_stats(self):
        print("current point -> x {} y {} ::: next point - > x {} y {} ".format(self.x, self.y, self.prev_x, self.prev_y))


##################### Manage Words and CSV files ###########################
def fillScoreMatrix(n,m,scoreMat, targetString, sourceString):
    n,m = n+1,m+1
    i,j = n,m


    traceback_list = []
    counter = 0
    node_list = []

    for i in range(1,n):
        for j in range(1,m):
            scoreMat[i][j], new_row, node = return_min(i, j,scoreMat, targetString, sourceString)
            traceback_list.append(new_row)
            node_list.append(node)
    return scoreMat, traceback_list, node_list

def return_min(i, j, matrix, targetString, sourceString):
    sourceLetter = ord(sourceString[i-1]) -96
    targetLetter = ord(targetString[j-1]) - 96
    #print(sourceString[i-1], sourceLetter)
    #print("source letter {} target letter {}".format(sourceString[i-1], targetString[j-1]))
    add = 0
    gap_penalty = 1
    left = matrix[i-1,j] + 1 # delete cost of source(i)
    up = matrix[i,j-1] + 1 # ins cost of target(j)
    diag = matrix[i-1,j-1] + leviObj.getCost(sourceLetter,targetLetter)
    #print(diag)
    #print(leviObj.getCost(sourceLetter,targetLetter))

    new_row = []
    new_row_dict ={"left":left,"up":up,"diag":diag}
    min_val = 1000
    key_value = ""
    for k,v in new_row_dict.items():
        if v < min_val:
            min_val = v
            key_value = k
    for key, value in new_row_dict.items():
        if value == min_val:
            new_row.append(key)
    print(new_row)

    node = TraceObj(i,j)
    node.direction_list = new_row
    node.set_dir()
    new_row.append(i)
    new_row.append(j)

    min_val = min(diag,left,up)
    return min_val, new_row, node


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
    f = open(file, 'r')
    lev =  csv.reader(f, delimiter=',')
    rows = [row for row in lev]
    return rows

def traceback(path_list, top_seq_col, left_seq_row):
    new_seq1 = ""
    new_seq2 = ""


    seq1 = "Z";seq2 = "Z"
    seq1 += top_seq_col ; seq2 += left_seq_row
    seq1_len = len(seq1) ; seq2_len = len(seq2)

    print(seq1)
    path_node = path_list[0]
    path_node.print_stats()
    for idx in range(1,len(path_list)):
        path_node - path_list[idx]
        print(path_node.sub_x)
        if path_node.sub_x >= 1:
             new_seq1 += (seq1[path_node.x])
             print(new_seq1)
        else:
            new_seq1 += "-"
        if path_node.sub_y >= 1:
            print(seq2[path_node.y])
            print("New sequence 2 {}".format(seq2))
            #new_seq2 += (seq2[path_node.y])
    #     else:
    #         new_seq2 += "-"
    #     path_node = path_list[idx]
    return new_seq1, new_seq2
if __name__ == '__main__':
    main()
