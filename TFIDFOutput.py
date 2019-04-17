"""Get TF-IDF results for all parshiot and then output to file parshiot with highest TF-IDF results -> essentially
generating topic lists/ relevant items for each parsha"""

import csv
from BazakAttack import TFIDF
from BazakAttack import Parshiot

# TODO:simplify code into one method

subDir = 'Results\\'


# write top TFIDF results to a csv
def TFIDFOutput(lang='heb'):
    parshiot = Parshiot.createSplitParshiot(lang)
    parshaResults = {}

    with open(subDir+'parshaResults'+lang+'.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['parsha', 'most relevant words']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for parsha in parshiot.keys():
            parshaResults[parsha] = TFIDF.parshaIDF(parsha, parshiot).most_common(20)
            writer.writerow({'parsha': parsha,
                             'most relevant words': [a[0] for a in parshaResults[parsha]]})


def hebrewFreqParshiot():
    parshiot = Parshiot.processParshiotByFrequency()
    parshaResults = {}

    with open(subDir+'TFIDFparshaResultsHebFreq.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['parsha', 'most relevant words']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for parsha in parshiot.keys():
            parshaResults[parsha] = TFIDF.parshaIDF(parsha, parshiot).most_common(20)
            writer.writerow({'parsha': parsha,
                             'most relevant words': [a[0] for a in parshaResults[parsha]]})



def main():
    TFIDFOutput()
    TFIDFOutput('en')
    hebrewFreqParshiot()




