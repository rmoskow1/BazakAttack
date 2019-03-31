"""Using TF-IDF on english and hebrew texts"""

from BazakAttack import TFIDF
from BazakAttack import Parshiot


def englishChapter():
    TEXT_NAME = 'JPS-Devarim.txt'
    chapterNum = 1
    print("Calculating chapter TF-IDF for ", TEXT_NAME, "in chapter ", chapterNum)
    print(TFIDF.chapterIDF(chapterNum, TEXT_NAME))

def hebrewParshiot():
    parshiot = Parshiot.parshiotSplit()
    print(TFIDF.parshaIDF('Chayei Sara', parshiot))


hebrewParshiot()












