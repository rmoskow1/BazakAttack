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
import Parshiot

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


# create a dictionary of TF values for each word in the hebrew text
def _TFCalculteHebrew(full_text_array):
    # hebrew text is already tokenized from Parshiot.py

    TF = Counter(full_text_array)

    # divide by total number of words
    textLength = len(full_text_array)
    for each in TF:
        TF[each] /= textLength

    # return the TF dictionary containing each word and its relative frequency
    return TF


# create a dictionary of TF values for each word in the hebrew text, calculated by 2 letter frequency values of text
def _TFCalculteHebrewFreq(full_text_array, freq_text_array):
    # hebrew text is already tokenized from Parshiot.py

    # count the frequencies in the 2 letter words
    TF = Counter(freq_text_array)

    # divide by total number of words
    textLength = len(freq_text_array)
    for each in TF:
        TF[each] /= textLength

    # create a counter for the full words. Set each TF to the TF of the 2 letter word calculated before
    TFFinal = Counter(full_text_array)

    for word in TFFinal:
        freqWord = Parshiot.processWordByFrequency(word)
        TFFinal[word] = TF[freqWord]

    # return the TF dictionary containing each word and its relative frequency
    return TFFinal



# assumes textCollection is a collection of arrays of text
# calculate the IDF for an individual word
def _IDFCalculate(textCollection, word):
    num_documents_with_word = 0
    for each in textCollection:
        if word in textCollection[each]:
            num_documents_with_word+=1
    if num_documents_with_word >0:
        return math.log(len(textCollection)/num_documents_with_word)
    return 1


# return a dictionary of each word in the single text as the key, with its corresponding TD-IDF value
def TFIDF(singleText, textCollection, lang='english'):
    if lang == 'hebrew': TFIDF = _TFCalculteHebrew(singleText)
    else:
        TFIDF = _TFCalculte(singleText)
    for each in TFIDF:
        TFIDF[each] *= _IDFCalculate(textCollection, each)
    return TFIDF


# currently only expecting hebrew text
def TFIDFFreq(singleText, freqTextcollection, freqSingleText):

    # calculate TFIDF using values from the frequency collection - the text converted to 2 letters words of the rarest
    # frequency

    TFIDF = _TFCalculteHebrewFreq(singleText, freqSingleText)

    # use the idf value of the frequency word
    for each in TFIDF:
        TFIDF[each] *= _IDFCalculate(freqTextcollection, Parshiot.processWordByFrequency(each))
    return TFIDF

# expecting text of english bible organized by chapters
def chapterIDF(chapterNum, TEXT_NAME):
    f = open(TEXT_NAME, 'rU')
    raw = f.read()

    # split the text on the regex below to match every Chapter
    rawTextChapters = re.split(r'Chapter\s\d+', raw)
    return TFIDF(rawTextChapters[chapterNum], rawTextChapters)


# expecting tokenized hebrew text organized by parshiot
def parshaIDF(parshaName, parshiot):
    return TFIDF(parshiot[parshaName], parshiot, 'hebrew')


# expecting tokenized hebrew text organized by parshiot
def parshaFreqIDF(parshaName, parshiot, freqParshiot):
    freqTFIDF = TFIDF(freqParshiot[parshaName], freqParshiot, 'hebrew')
    regTFIDF = Counter(parshiot[parshaName])
    for word,value in regTFIDF.items():
        regTFIDF[word] = freqTFIDF[Parshiot.processWordByFrequency(word)]
    return regTFIDF








