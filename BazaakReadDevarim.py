"""The following is the initial implementation of the Bazaak method of categorizing biblical sections. R' Bazaak
uses repetition of significant words as indicative of a section break i.e. if there's repetition of a word MIN_WORD_COUNT
number of times within MIN_DISTANCE of the text, then that defines a section of a text. Here, the text of Deuteronomy
is used. """

import nltk
import numpy

# minimum distance allowed between start and end of the section
MIN_DISTANCE = 30

# minimum amount of word instances required to define a section
MIN_WORD_COUNT = 3

# initial implementation is using only the text of Deuteronomy
f = open('JPS-Devarim.txt', 'rU')
raw = f.read()
tokens = nltk.word_tokenize(raw)
text = nltk.Text(tokens)

# collection of each word in the text
unique_words = set(tokens)

full_text_array = numpy.array(tokens)


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
    return [start, end]


print("Calculating all sections within the text....")
print()

# generate list of indeces for where each word is found
for each in unique_words:
    indeces = numpy.where(full_text_array == each)[0]
    # check if there are the minimum number of word instances
    if len(indeces) > MIN_WORD_COUNT:
        # if min distance between first and last is less than min distance, save indeces as a section
        section = _findSection(indeces)
        if section:
            print("******", each, "******")
            # print the section from the original text
            for i in range(indeces[section[0]], indeces[section[1]], 1):
                print(full_text_array[i], end =" ")
            print("")








