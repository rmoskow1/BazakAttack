"""The following analyzes Biblical text with TF-IDF.
TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
IDF(t) = log_e(Total number of documents / Number of documents with term t in it)
Here, total documents could be interpreted in several different ways:
  -> single document: single verse in the text. total documents: total number of verses (in a Chapter, in a Book, or in 
     all of the text)
  -> single document: single Chapter. total documents: total chapters (in a Parsha, in book, or in all the text)
  -> single document: single Parsha. total documents: total Parshas (in a book, or in all of the text)
"""


#http://www.tfidf.com/

import nltk
import numpy
import math
from collections import Counter
import re


# create a dictionary of TF values for each word in the text
def _TFCalculte(rawText):
    tokens = nltk.word_tokenize(rawText)
    text = nltk.Text(tokens)

    full_text_array = numpy.array(tokens)

    # create a dictionary with total word frequency
    TF = Counter(full_text_array)

    # divide by total number of words
    textLength = len(full_text_array)
    for each in TF:
        TF[each] /= textLength

    # return the TF dictionary containing each word and its relative frequency
    return TF


# assumes textCollection is a collection of arrays of text
# calculate the IDF for an individual word
def _IDFCalculate(textCollection, word):
    num_documents_with_word = 0
    # TODO: global cache for if the word was already found in their
    for each in textCollection:
        if word in each:
            num_documents_with_word+=1
    if num_documents_with_word >0:
        return math.log(len(textCollection)/num_documents_with_word)
    # TODO: determine appropriate behavior for return when the number of documents is 0
    return 1


# return a dictionary of each word in the single text as the key, with its corresponding TD-IDF value
def TFIDF(singleText, textCollection):
    TFIDF = _TFCalculte(singleText)
    for each in TFIDF:
        TFIDF[each] *= _IDFCalculate(textCollection, each)
    return TFIDF



def chapterIDF(chapterNum, TEXT_NAME):
    f = open(TEXT_NAME, 'rU')
    raw = f.read()

    # split the text on the regex below to match every Chapter
    rawTextChapters = re.split(r'Chapter\s\d+', raw)
    return TFIDF(rawTextChapters[chapterNum], rawTextChapters)




def main():
    TEXT_NAME = 'JPS-Devarim.txt'
    chapterNum = 1
    print("Calculating chapter TF-IDF for ", TEXT_NAME, "in chapter ", chapterNum)
    print(chapterIDF(chapterNum, TEXT_NAME))

main()












