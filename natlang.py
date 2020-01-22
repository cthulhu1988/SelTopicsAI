#!/usr/bin/env python3
import tkinter as tk
import nltk
from nltk.book import *

def main():
    print("------------------------------------")
    fdist1 = FreqDist(text3)
    print(fdist1)
    #print(fdist1.plot())
    #print(fdist1.most_common(50))
    #fdist1.plot(50, cumulative=True)

    #print("hapaxes {}".format(fdist1.hapaxes()))
    V = set(text1)
    #long_words = [w for w in V if len(w) > 17]
    #print(long_words)

    fdistMoby = FreqDist(text1)
    common_words = [w for w in V if len(w) > 3 and fdistMoby[w] > 60]
    #print(common_words)
    #print('; '.join(text1.collocation_list()))

    # print random text from the source material:
    ###text1.generate()


    # ends with or starts with:
    end_with = sorted([w for w in set(text1) if w.endswith('ableness')])
    print(end_with)

def lexical_richness(text, word="smote"):
    total_words = (len(text))
    unique_words = len(set(text))
    print("Name: {}".format(text))
    print("lexical richness {}".format(unique_words/total_words))
    if word != "smote":
        count = text.count(word)
        print("Percentate of text that is {} is {}".format(word, count/total_words*100))

def print_details(text):
    print("Name: {}".format(text))
    total_words = (len(text))
    print("Number of all words: {}".format(total_words))
    unique_words = len(set(text))
    print("Number of unique words: {}".format(unique_words))

def find_word(text=text1, word="monstrous"):
    print("finding the word {} in the text {}".format(word, text))
    print("------------------All examples--------------------")
    text.concordance(word)
    print("------------------END-----------------------------")

def print_set(text):
    print("------------------Start Set--------------------")
    print(sorted(set(text)))
    print("------------------END SET-----------------------------")


if __name__ == '__main__':
    main()
