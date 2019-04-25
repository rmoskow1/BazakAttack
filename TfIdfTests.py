"""Using TF-IDF on english and hebrew texts"""

from BazakAttack import TFIDF
from BazakAttack import Parshiot


def englishChapter():
    TEXT_NAME = 'JPS-Devarim.txt'
    chapterNum = 1
    print("Calculating chapter TF-IDF for ", TEXT_NAME, "in chapter ", chapterNum)
    print(TFIDF.chapterIDF(chapterNum, TEXT_NAME))


PARSHA_NAME = 'Toldot'

def englishParshiot():
    parshiot = Parshiot.createSplitParshiot('en')
    print("Calculating regular english TD-IDF for ", PARSHA_NAME)
    results = TFIDF.parshaIDF(PARSHA_NAME, parshiot)
    print(results)
    print("20 most common:")
    print(results.most_common(20))


def hebrewParshiot():
    parshiot = Parshiot.createSplitParshiot()
    print("Calculating regular hebrew TD-IDF for ", PARSHA_NAME)
    results = TFIDF.parshaIDF(PARSHA_NAME, parshiot)
    print(results)
    print("20 most common:")
    print(results.most_common(20))

def hebrewParshiotWithFreq():
    parshiot = Parshiot.createSplitParshiot()
    parshiotFreq = Parshiot.processParshiotByFrequency()
    print("Calculating hebrew TD-IDF for ", PARSHA_NAME, " based on minimum letter frequency")
    results = TFIDF.parshaFreqIDF(PARSHA_NAME, parshiot, parshiotFreq)
    print(results)
    print("20 most common:")
    print(results.most_common(20))

def hebrewParshiotTop():
    parshiot = Parshiot.createSplitParshiot()
    print("Calculating regular hebrew TD-IDF for ", PARSHA_NAME)
    results = TFIDF.parshaIDF(PARSHA_NAME, parshiot)
    print(results)
    print(len(results))
    percent = int(len(results)/2)
    print("top 50% of results: ", percent)
    print(results.most_common(percent))
    r = results.most_common(percent)
    l = [i[0] for i in r]
    print(l)


def testingSingleParsha():
    englishParshiot()
    hebrewParshiot()
    hebrewParshiotWithFreq()
    hebrewParshiotTop()


















