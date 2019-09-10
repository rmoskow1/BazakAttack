import Parshiot, BazaakRead
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


def BazaakFilteredOutput(lang = 'heb', min_count=5, parshaResults = None, fileName=None):
    if not fileName:
        fileName = subDir + lang + 'Bazaak' + 'TFIDFOutput' + '.csv'
    parshaNames = Parshiot.parshaNames()
    if not parshaResults:
        parshaResults = BazaakAll(lang, min_count, filtered=True)

    with open(fileName, mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['parsha', 'repeated important words']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for parsha in parshaNames:
            writer.writerow({'parsha': parsha,
                             'repeated important words': list(parshaResults[parsha].keys())})


# perform a bazaak read for all parshiot and return a dictionary with parsha names as key and bazaak read results as
# values
# only return filtered by tf-idf values if filtered = True
# use strippedDown hebrew if strippedDown = True
def BazaakAll(lang = 'heb', min_count=5, min_distance=80, filtered= False, strippedDown=True):
    if strippedDown:
        parshiot = Parshiot.processParshiotByFrequency()
    else: parshiot = Parshiot.createSplitParshiot(lang)
    parshaResults = {}
    if filtered: # filter with TF-IDF results
        for parsha in parshaNames:
            parshaResults[parsha] = BazaakRead.filterBazaakParshaReadTFIDF(parsha, lang,
                                                                           min_count, parshiot, min_distance)
    else:
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
# or, if filtering, plot the bazaak count comparison per parsha between the original and filtered results
def plotCountComparison(countResults, filtering=False, lang='heb'):
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
    plt.xticks(rotation='90')
    plt.tight_layout()

    # if this is TF-IDF filtering, name accordingly
    if filtering:
        ax.legend((rects1[0], rects2[0]), ('Original', 'Filtered'))
        fileName = subDir +lang +'TFIDFfilteringCountDifferences'+'.pdf'
    else:
        ax.legend((rects1[0], rects2[0]), ('Hebrew', 'English'))
        fileName = subDir+'langLeitwortCountDifferences.pdf'

    plt.show()
    fig.savefig(fileName)


# plot the different bazaak count results, per parsha, based on the different minimum word count requirements
def plotVariedMinCountResults(results, lang='heb'):
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
    plt.xticks(rotation='90')

    ax.legend((rects1[0], rects2[0], rects3[0]), ('5', '6', '7'))
    plt.show()
    fig.savefig(subDir+'leitwortMinCountDifferences'+lang+'.pdf')


# write all the leitworts for all the texts, with default leitwort parameters to csv
def writeBazaakToCSV():
    BazaakOutput()
    BazaakOutput('en')
    BazaakOutput(parshaResults = BazaakAll(strippedDown=True), fileName= subDir+"strippedHebBazaakOutput.csv")


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
    plotVariedMinCountResults(variedHebCountResults)
    plotVariedMinCountResults(variedEnCountResults, 'en')


# plot the variations of leitwort counts per parsha comparing all results to only results filtered by TF-IDF
# significance
def variedFilteredTFIDFCounts(lang='heb'):
    countResults = {}

    allResults = BazaakAll(lang=lang)
    filteredResults = BazaakAll(lang=lang, filtered=True)
    for parsha in parshaNames:
        countResults[parsha] = [len(allResults[parsha]), len(filteredResults[parsha])]

    # plot the differences in count, before and after TF-IDF filtering
    plotCountComparison(countResults, filtering=True, lang=lang)




# produce results for a different minimum distance
def testNewDistance(min_distance):
    hebResults = BazaakAll(min_distance=min_distance)
    fileNameHeb = subDir+'heb'+'Bazaak'+'Output'+ str(min_distance) +'.csv'
    engResults = BazaakAll(lang='en', min_distance=min_distance)
    fileNameEng = subDir+'en'+'Bazaak'+'Output'+ str(min_distance) +'.csv'
    BazaakOutput(parshaResults=hebResults, fileName=fileNameHeb)
    BazaakOutput(lang='en', parshaResults=engResults, fileName=fileNameEng)



def main():

    # output Bazaak results in english and hebrew with default values to CSV files
    writeBazaakToCSV()

    # plot the differences in english and hebrew leitwort counts with default values and save in Results
    variedHebrewEnglishCounts()

    # test increasing the minimum distance for leitworts in english and hebrew
    testNewDistance(90)

    # plot the differences in changing the minimum word count for leitworts
    variedMinWordCounts()

    # do Bazaak reads with TF-IDF filtering
    BazaakFilteredOutput() # hebrew
    BazaakFilteredOutput(lang='en') # english

    # plot the differences in results with TF-IDF filtering vs original
    variedFilteredTFIDFCounts(lang='en')
    variedFilteredTFIDFCounts()











