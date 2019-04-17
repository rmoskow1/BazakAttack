from BazakAttack import Parshiot, BazaakRead
import csv
import numpy as np
import matplotlib.pyplot as plt


hebResults = None
engResults = None
parshaNames = Parshiot.parshaNames()
subDir = 'Results\\'


# write bazaak results to a CSV file with parsha as column one and list of words as column 2
# option to pass in parshaResults (helpful if already generated, such as in the main here
def BazaakOutput(lang = 'heb', min_count=5, parshaResults = None, fileName=None):
    if not fileName:
        fileName = subDir+lang+'Bazaak'+'Output'+'.csv'
    parshaNames = Parshiot.parshaNames()
    if not parshaResults:
        parshaResults = BazaakAll(lang, min_count)

    with open(fileName, mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['parsha', 'repeated words']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for parsha in parshaNames:
            writer.writerow({'parsha': parsha,
                             'repeated words': list(parshaResults[parsha].keys())})


# perform a bazaak read for all parshiot and return a dictionary with parsha names as key and bazaak read results as
# values
def BazaakAll(lang = 'heb', min_count=5, min_distance=80):
    parshiot = Parshiot.createSplitParshiot(lang)
    parshaResults = {}
    for parsha in parshaNames:
        parshaResults[parsha] = BazaakRead.BazaakParshaRead(parsha, lang, min_count, parshiot, min_distance)
    return parshaResults


# return a dictionary of parsha names as key and list of the number of leitworts returned from the hebrew results
# and the english results as value
def compareCounts(hebResults, engResults):
    countResults = {}
    for parsha in hebResults:
        countResults[parsha] = [len(hebResults[parsha]), len(engResults[parsha])]
    return countResults


# plot the bazaak count comparision per parsha between the english and the hebrew
def plotCountComparison(countResults):
    N = len(parshaNames)
    results = list(zip(*countResults.values()))

    ind = np.arange(N)  # the x locations for the groups
    width = 0.40  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, results[0], width, color='r')

    rects2 = ax.bar(ind + width, results[1], width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Total leitworts')
    ax.set_title('Compare Leitwort Counts')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(parshaNames)
    plt.xticks(rotation='45')
    plt.tight_layout()

    ax.legend((rects1[0], rects2[0]), ('Hebrew', 'English'))
    plt.show()

    fig.savefig(subDir+'langLeitwortCountDifferences.pdf')


# plot the different bazaak count results, per parsha, based on the different minimum word count requirements
def plotVariedCountResults(results, lang='heb'):
    N = len(parshaNames)

    # results are now the count of words for each parsha, and each list entry is for a different minimum word count
    results = list(zip(*results.values()))

    ind = np.arange(N)
    width = 0.20

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind-width, results[0], width, color='r')

    rects2 = ax.bar(ind, results[1], width, color='y')

    rects3 = ax.bar(ind + width, results[2], width, color='g')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Total leitworts')
    ax.set_title('Compare Varied Minimum Leitwort Counts '+ lang)
    ax.set_xticks(ind + width*2 / 2)
    ax.set_xticklabels(parshaNames)
    plt.xticks(rotation='45')

    ax.legend((rects1[0], rects2[0], rects3[0]), ('5', '6', '7'))
    plt.show()

    fig.savefig(subDir+'leitwortMinCountDifferences'+lang+'.pdf')


def writeBazaakToCSV():
    BazaakOutput()
    BazaakOutput('en')


# plot the differences in count between the hebrew and the english per parsha
def variedHebrewEnglishCounts():
    hebResults = BazaakAll()
    engResults = BazaakAll('en')
    countResults = compareCounts(hebResults, engResults)
    plotCountComparison(countResults)


# plot hebrew and english variations per parsha of leitwort count, based on varied minimum word count requirement
def variedMinWordCounts():
    hebResults = []
    engResults = []

    # use minimum word count 5, 6, and 7
    for i in range(5,8):
        hebResults.append(BazaakAll(min_count=i))
        engResults.append(BazaakAll(lang='en', min_count=i))
    variedEnCountResults = {}
    variedHebCountResults = {}

    for parsha in parshaNames:
        # these dictionaries will contain parsha as key, list of the different leitwort counts as values
        variedHebCountResults[parsha] = []
        variedEnCountResults[parsha] = []
        for i in range(3):
            variedHebCountResults[parsha].append(len(hebResults[i][parsha]))
            variedEnCountResults[parsha].append(len(engResults[i][parsha]))

    # plot the hebrew and the english results separately
    plotVariedCountResults(variedHebCountResults)
    plotVariedCountResults(variedEnCountResults, 'en')


# produce results for a different minimum distance
def testNewDistance(min_distance):
    hebResults = BazaakAll(min_distance=min_distance)
    fileNameHeb = subDir+'heb'+'Bazaak'+'Output'+ str(min_distance) +'.csv'
    engResults = BazaakAll(lang='en', min_distance=min_distance)
    fileNameEng = subDir+'en'+'Bazaak'+'Output'+ str(min_distance) +'.csv'
    BazaakOutput(parshaResults=hebResults, fileName=fileNameHeb)
    BazaakOutput(lang='en', parshaResults=engResults, fileName=fileNameEng)


def main():

    writeBazaakToCSV()
    variedHebrewEnglishCounts()
    testNewDistance(90)
    variedMinWordCounts()








