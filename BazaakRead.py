"""Find significant words in a text following method by R' Bazaak (and Yeshivat Har Etzion) using word repition.
If there's repetition of a word MIN_WORD_COUNT of times within MIN_DISTANCE - there's a significance to the word and the
section. """

from BazakAttack import Parshiot
import numpy


MIN_DISTANCE = 80
MIN_WORD_COUNT = 3

# for a given text, find all the significant words - the words that are repeated within the appropriate distance
# return a dictionary with significant words as keys and the indeces where they occur in the text as values
def BazaakRead(text):
    indeces = _indeces(text)
    significantWords = {}
    # for each unique word in the text
    for word in indeces:
        # if there are the minimum number of counts of the word to be considered significant, continue
        if len(indeces[word])> MIN_WORD_COUNT:
            sectionIndeces = _findSection(indeces[word])
            if sectionIndeces: significantWords[word] = indeces[word][sectionIndeces[0]:sectionIndeces[1]]
    return significantWords


# for a given parsha, do a bazaak read. Set language to be used
def BazaakParshaRead(parshaName, lang='heb'):
    splitParshiot = Parshiot.createSplitParshiot(lang)
    parsha = splitParshiot[parshaName]
    return BazaakRead(parsha)


# for a given parsha, perform a bazaak read with all occurances of the infrequent 2 letters
def freqBazaakParshaRead(parshaName):
    freqParshiot = Parshiot.processParshiotByFrequency()
    parsha = freqParshiot[parshaName]
    return BazaakRead(parsha)


# for a given text (assuming a list of words, tokenized) return a dictionary of the unique words and the indeces
# of where each word is found in the text
def _indeces(text):
    unique_words = set(text)
    indeces_list = {}
    full_text = numpy.array(text)
    # generate list of indeces for where each word is found
    for word in unique_words:
        indeces = list(numpy.where(full_text == word)[0])
        indeces_list[word] = indeces
    return indeces_list

# helper function to check a list of indeces for a section - where at least the minimum number
# of words are located within the maximum allowed word distance i.e. section length
def _findSection(indeces):
    i = 0
    start = 0
    end = MIN_WORD_COUNT

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

    # start and end now represent the indeces of the first largest collection of the word within the minimum
    # allowed distance
    # TODO: check if there's a second set of significant appearences of this word in the collection
    return [start, end]


def main():
    # perform a bazaak read for parsha Chayei Sara
    print("Finding signifcant words in Chayei Sara for min words=", MIN_WORD_COUNT, " and min distance=", MIN_DISTANCE)
    print(BazaakParshaRead('Chayei Sara'))
    print(BazaakParshaRead('Chayei Sara', 'en'))
    print("Finding significant freqWords in Chayei Sara")
    print(freqBazaakParshaRead('Chayei Sara'))


main()



