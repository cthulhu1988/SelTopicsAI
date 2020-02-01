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

########################### CLASSES ###########################





########################### FUNCTIONS ###########################
def openTXTFile(file):
    with open(file, encoding="ISO-8859-1") as fp:
        line = fp.readline()
        line.strip("'")
        while line:
            line = fp.readline()
            line_list = line.split()
            pattern = "[A-Za-z0-9]"
            words = [word for word in line_list if re.search(pattern,word)]
            print(words)

if __name__ == '__main__':
    main()
