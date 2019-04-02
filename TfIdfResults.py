"""Using TF-IDF on english and hebrew texts"""

from BazakAttack import TFIDF
from BazakAttack import Parshiot


def englishChapter():
    TEXT_NAME = 'JPS-Devarim.txt'
    chapterNum = 1
    print("Calculating chapter TF-IDF for ", TEXT_NAME, "in chapter ", chapterNum)
    print(TFIDF.chapterIDF(chapterNum, TEXT_NAME))


PARSHA_NAME = 'Chayei Sara'


def hebrewParshiot():
    parshiot = Parshiot.parshiotSplit()
    print("Calculating regular hebrew TD-IDF for ", PARSHA_NAME)
    results = TFIDF.parshaIDF(PARSHA_NAME, parshiot)
    print(results)
    print("20 most common:")
    print(results.most_common(20))

def hebrewParshiotWithFreq():
    parshiot = Parshiot.parshiotSplit()
    parshiotFreq = Parshiot.processParshiotByFrequency()
    print("Calculating hebrew TD-IDF for ", PARSHA_NAME, " based on minimum letter frequency")
    results = TFIDF.parshaFreqIDF(PARSHA_NAME, parshiot, parshiotFreq)
    print(results)
    print("20 most common:")
    print(results.most_common(20))


hebrewParshiot()
hebrewParshiotWithFreq()











