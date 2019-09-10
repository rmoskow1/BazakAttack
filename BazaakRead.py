"""Find significant words in a text following method by R' Bazaak (and Yeshivat Har Etzion) using word repition.
If there's repetition of a word MIN_WORD_COUNT of times within MIN_DISTANCE - there's a significance to the word and the
section. """

import Parshiot, TFIDF

# minimum distance between start and end of word repetitions
MIN_DISTANCE = 80
# minimum number of words required to be repeated to determine a leitwort
MIN_WORD_COUNT = 5
# percent of TF-IDF to filter by. (For only leitworts that were within the top PERCENT% of TF-IDF scoring words for the
# parsha)
PERCENT = 50

# for a given text, find all the significant words - the words that are repeated within the appropriate distance
# return a dictionary with significant words as keys and the indeces where they occur in the text as values
def BazaakRead(text, min_count = MIN_WORD_COUNT, min_distance=MIN_DISTANCE):
    indeces = _indices(text)
    significantWords = {}
    # for each unique word in the text
    for word in indeces:
        # if there are the minimum number of counts of the word to be considered significant, continue
        if len(indeces[word])>= min_count:
            sectionIndeces = _findSection(indeces[word], min_count)
            if sectionIndeces:
                significantWords[word] = {
                    'section': indeces[word][sectionIndeces[0]:sectionIndeces[1]+1],
                    'all locations': indeces[word]}
    return significantWords


# for a given parsha, do a bazaak read.
# parameters: lang - language to be used (default is the hebrew), min_count - minimum word count required to define a
# leitwort, default is the defined above, splitParshiot - option to create the parshiot outside the function and pass
# them in, particularly helpful when calling the function multiple times, min_distance - minimum distance (section
# length) for a leitwort, default is defined above
def BazaakParshaRead(parshaName, lang='heb', min_count=MIN_WORD_COUNT, splitParshiot=None, min_distance=MIN_DISTANCE):
    if not splitParshiot:
        splitParshiot = Parshiot.createSplitParshiot(lang)
    parsha = splitParshiot[parshaName]
    return BazaakRead(parsha, min_count, min_distance)


# for a given parsha, perform a bazaak read with all occurences of the infrequent 2 letters
# option to create the frequency parshiot outside of the function and pass in, particularly helpful if the function is
# being called multiple times
def freqBazaakParshaRead(parshaName, freqParshiot = None, min_count=MIN_WORD_COUNT, min_distance=MIN_DISTANCE):
    if not freqParshiot:
        freqParshiot = Parshiot.processParshiotByFrequency()
    parsha = freqParshiot[parshaName]
    return BazaakRead(parsha, min_count, min_distance)


# do a bazaak read that is then "filtered" by TF-IDF results. Only use the words which are in the top %50 percent of the
# scored TF-IDF words
def filterBazaakParshaReadTFIDF(parshaName, lang='heb', min_count=MIN_WORD_COUNT,
                                splitParshiot=None, min_distance=MIN_DISTANCE):
    if not splitParshiot:
        splitParshiot = Parshiot.createSplitParshiot(lang)

    topTFIDF = TFIDF.parshaIDF(parshaName, splitParshiot)
    totalWords = len(topTFIDF)

    # find the percentage needed
    percent = PERCENT / 100

    topTFIDF = topTFIDF.most_common(int(totalWords*percent))

    # just get the keys, the words
    topTFIDF = [i[0] for i in topTFIDF]

    parsha = splitParshiot[parshaName]
    read = BazaakRead(parsha, min_count, min_distance)

    # create a new dictionary, only containing results where the key was in the top PERCENT% of TF-IDF scores
    newRead = {k: v for k, v in read.items() if k in topTFIDF}

    return newRead


# for a given text (assuming a list of words, tokenized) return a dictionary of the unique words and the indeces
# of where each word is found in the text
def _indices(text):
    unique_words = set(text)
    indices_list = {}
    # generate list of indices for where each word is found
    for word in unique_words:
        indices = [index for index, value in enumerate(text) if value == word]
        indices_list[word] = indices
    return indices_list


# helper function to check a list of indices for a section - where at least the minimum number
# of words are located within the maximum allowed word distance i.e. section length
def _findSection(indeces, min_count):
    i = 0
    start = 0
    end = min_count-1

    # find the beginning of the section

    # while we haven't found bookends of the minimum distance for a section, continue
    while indeces[end] - indeces[start] > MIN_DISTANCE:
        # roll the section we're analyzing over by one
        start +=1
        end +=1
        # check that we haven't reached the end of the list. If so, return None. There's no section
        if end > len(indeces)-1: return None

    # if this point has been reached, a start and end point has been found for a section. But it's possible
    # the same section contains more than the minimum number of words. Continue to roll the end, while
    # maintaining the beginning

    foundEnd = False
    while foundEnd == False and end < len(indeces)-2:
        end +=1
        if indeces[end]-indeces[start] > MIN_DISTANCE:
            end -=1
            foundEnd = True

    # start and end now represent the indices of the FIRST largest collection of the word within the minimum
    # allowed distance
    return [start, end]


def testParsha():
    # perform a bazaak read for a parsha
    parsha = 'Bereshit'
    lang = 'heb'
    print("Finding signifcant words in ", parsha, " for min words=", MIN_WORD_COUNT, " and min distance=", MIN_DISTANCE)
    print(BazaakParshaRead(parsha, lang).keys())

    print(len(BazaakParshaRead(parsha, lang)))
    print(BazaakParshaRead(parsha, lang))

    print("Testing the tfidf filtering...")
    print(len((filterBazaakParshaReadTFIDF(parsha, lang).keys())))

    print((filterBazaakParshaReadTFIDF(parsha, lang).keys()))

testParsha()






