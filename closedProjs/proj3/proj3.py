#!/usr/bin/env python
# coding: utf-8
import random
from nltk.classify import NaiveBayesClassifier
from nltk import classify
from nltk.metrics import *
import collections

sotu_file = 'sotu.txt'
pres_by_party = 'presidentsbyparty.txt'

repub_list = [] ; dem_list = []

with open(pres_by_party) as prez:
    cl = prez.readline()
    cl = cl.strip()
    if (cl == 'Republican'):
        while cl != 'Democrat':
            cl = prez.readline()
            cl = cl.strip()
            if len(cl) > 1:
                repub_list.append(cl)
    repub_list = repub_list[:-1]
    for line in prez:
        if len(line) > 1:
            line = line.strip()
            dem_list.append(line)
     
#sotu = open(sotu_file,'r')
# shift + tab shows documenation. 

testFile = open("test.txt","w+")

with open(sotu_file) as sf:
    line = sf.readline()
    while line: # while there is a line on sotu

        line = line.strip() # strip white space from line
        if '@' in line: # if at beginning of speech
            line = line.split('@',4) # pull out pres name
            name = line[1] # pres name
            if name in repub_list: # if line is start of a pres speech we care about
                testFile.write("@"+name+'\n')
                line = sf.readline() # read the next line
                line = line.strip() # strip whitespace 
                while '@' not in line: # while we are in speech
                    testFile.write(line) # write out line
                    line = sf.readline() # read next
            elif name in dem_list:
                print(name)
        line = sf.readline()
        
testFile.close()
print("Done in this section")





