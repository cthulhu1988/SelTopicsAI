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
    global leviObj
    global confObj
    leviObj = matrixObj(openCSVFile(leviDistance)); confObj = matrixObj(openCSVFile(confDistance))
    wordObjList = (openTXTFile(wordList))

    for y, wObj in enumerate(wordObjList):
    ############ LOOP THROUGH ###################
        for x in range(wObj.getListLeng()):
            n,m = wObj.getSrcWordLeng(x), wObj.getTrgtLeng()
    # GET BACK intialized matrix.
            scrMatInit = scoreMatrixInit(n,m)
    # FINISH filling up the score matix. Change based on levinstein or confusion
            targetString = wObj.targetWord
            sourceString = wObj.sourceList[x]


            scrMatrix, cost, PMatrix = fillScoreMatrix(n,m,scrMatInit, targetString, sourceString, leviObj)
            final_seq1, final_seq2, changes = findSequences(PMatrix, targetString, sourceString)
            changes = changes[::-1]
            final_seq1 = final_seq1[::-1]
            final_seq2 = final_seq2[::-1]
            printFinalOutput(final_seq1, final_seq2, cost,changes)

            scrMatrix, cost, PMatrix = fillScoreMatrix(n,m,scrMatInit, targetString, sourceString, confObj)
            final_seq1, final_seq2, changes = findSequences(PMatrix, targetString, sourceString)
            changes = changes[::-1]
            final_seq1 = final_seq1[::-1]
            final_seq2 = final_seq2[::-1]
            printFinalOutput(final_seq1, final_seq2, cost,changes)

            print("-"*50)

def printFinalOutput(final_seq1, final_seq2, cost, changes):
    sepLeng = len(final_seq1)
    print(final_seq2)
    print("|"*sepLeng)
    print("{}".format(final_seq1))
    print("{} ({})".format(changes, cost))
    print()

######################### CLASSES ##########################

class matrixObj:
    def __init__(self, array):
        self.array = array
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
    def getSrcWordLeng(self, num=0):
        return len(self.sourceList[num])
    def getListLeng(self):
        return len(self.sourceList)
    def printList(self):
        #print("Target word is {}".format(self.targetWord))
        #print("Source Words are: ")
        for word in self.sourceList:
            print(word, end=" ")
        print()

####################FUNCTIONS###########################################################
def findSequences(PMatrix, targetString, sourceString):
    TRG_SEQ = ""; SRC_SEQ = ""; changes = ""
    i = len(targetString); j = len(sourceString)
    #print("target word {} and source word {}".format(targetString, sourceString))

    # navigate traceback array, start at bottom right.
    while i >= 0 or j >= 0:
        ########## RANDOMLY CHOOSE NEXT DIRECTION ######################
        list_pointer = [x for x in PMatrix[j][i]]
        rand_item = list_pointer[random.randrange(0,len(list_pointer))]
        # start buidling target string:
        i -=1
        if i >=0:
            TRG_SEQ += targetString[i]
            #print("TRG_SEQ {}".format(TRG_SEQ))
        ############ iterate through possible pointers ##############
        if rand_item == "\\":
            j-=1
            if j >=0:
                SRC_SEQ += sourceString[j]
                if sourceString[j] == targetString[i]:
                    changes += "k"
                else:
                    changes += "s"

        elif rand_item == "^":
            j-=1
            if j < 0:
                j = 0
            changes += "d"

        elif rand_item == "<":
            changes += "i"
            SRC_SEQ += "*"

        elif rand_item == "0":
            break

    #print("i {} and j {}".format(i,j))
    i-= 1; j -=1
    while i >= 0:
        SRC_SEQ += "*"
        TRG_SEQ += (targetString[i])
        changes += "d"
        i -= 1
    while j >= 0:
        SRC_SEQ += (sourceString[j])
        TRG_SEQ += ("*")
        changes += "d"
        j -= 1
    return TRG_SEQ,SRC_SEQ, changes

def fillScoreMatrix(n,m,scoreMat, targetString, sourceString, matrix_obj):
    n,m = n+1,m+1
    i,j = n,m

    pointer_list = []
    w, h = scoreMat.shape
    PMatrix = [["0" for x in range(h)] for y in range(w)]

    for i in range(1,n):
        for j in range(1,m):
            scoreMat[i][j], pointer = return_min(i, j,scoreMat, targetString, sourceString, matrix_obj)
            pointer_list.append(pointer)
            PMatrix[i][j] = pointer
    cost = (scoreMat[n-1][m-1])

    # for x in range(w):
    #     for y in range(h):
    #         print(PMatrix[x][y],end=" ")
    #     print()
    return scoreMat, cost, PMatrix

def return_min(i, j, matrix, targetString, sourceString, matrix_obj):

    targetLetter = ord(targetString[j-1])-96
    sourceLetter = ord(sourceString[i-1])-96
    left = matrix[i-1,j] + 1 # delete cost of source(i)
    up = matrix[i,j-1] + 1 # ins cost of target(j)
    diag = matrix[i-1,j-1] + matrix_obj.getCost(sourceLetter,targetLetter)
    new_row = []
    new_row_dict ={"<":left,"^":up,"\\":diag}
    min_val = 1000
    key_value = ""
    new_string = ""
    for k,v in new_row_dict.items():
        if v < min_val:
            min_val = v
            key_value = k

    for key, value in new_row_dict.items():
        if value == min_val:
            #new_row.append(key)
            new_string+=key
    #RAND_DIRECTION = new_row[random.randrange(0,len(new_row))]
    #print("direction choosen {}".format(RAND_DIRECTION))
    return min_val, new_string

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

if __name__ == '__main__':
    main()
'''
a) Compare and contrast the results obtained from using the different cost approaches. Is one “better” than the
other? How? Why?

ANSWER: The confusion matrix approach seem to output a lower cost as opposed to Levenshtein distance. The Levenshtein distance
is a generic approca to the issue, the confusion matrix appears to be highly specific, with commonly substituted letters
tabulated accoding to probability.

b) While the algorithm you implemented yields the minimum edit distance between a pair of words, it is not clear
how it fits into a larger context (e.g., where does it get the words from?). Provide a description of its plausible
use in a natural language application context (how does one arrive at the candidate words, how is the correct
spelling selected, etc.)

ANSWER: The minimum edit distance algorithm's plausible use case would be correcting mispelled words that are close to
a correct spelling. In this program we have "target" words and "source" words. Now the question arises as to how a word gets
designated as a target word? We must presumed that these target words are the correct according to whoever promulgates such
target words. So there must be a corpus of words deemed correct from which to compare mispelled words. General spell check has been present in systems for years. So if a system is attempting to identify a word, and the minimum edit distance is low with regard to another word, the system can guess that the target word with low edit distance was intended. This could be augmented with a N-Gram approach.

c) Explain how you might devise a new set of costs: what process would you go through? What data would you use
or collect? How would you arrive at final values for the table?

ANSWER: Of course the Levenshtein costs are generic, the confusion matrix costs are very specific. However, we don't know under
what circumstances these costs were developed. Are these mistakes with regard to a letter or character made because people are natrually bad spellers? Were these costs developed with errors stemming from certain types of keyboards? What about Mobile keyboards? I think if you were developing a new set of costs it would be a balance between errors made in general and erros made in highly specific circumstances. Not to mention considering the language or dialect utilized. With the advent of "Big Data" one could sort through the language corpus and collected data to gauge the error rate of certain activites. Google autocomplete seems to be a good example of that type of approach. However, would one even attempt to implement such a system in a chat application or a Twitter feed with the liberal abuse of the King's English so prevelent on such platforms? So in conclusion, the language, dialect, platform, and interface are all considerations when constructing a new cost matrix.     

'''

# From book:
    # TARGET -> TOP , Y, n, i
    # Source -> SIDE LEFT , X, m, j
    # n/i is leng of source X string and m/j in leng of Target Y string
    # source is the siderow X , target is the top Y row
