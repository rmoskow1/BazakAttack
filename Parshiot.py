"""Create a 2D array of text organized by Parsha and verse. i.e parshiot['Chayei Sarah'][0] returns
the first verse in the Parsha: Chayei Sarah from the Sefaria database text"""

from pymongo import MongoClient
from collections import OrderedDict, defaultdict
from BazakAttack import HebrewLetterFrequency

# version of the text being used
VERSION_TITLE_HEB = "Tanach with Text Only"
VERSION_TITLE_ENG = "The Holy Scriptures: A New Translation (JPS 1917)"


# process text from sefaria and create dictionary by parshiot for the english text
def createEngParshiot():
    return _createParshiot(VERSION_TITLE_ENG)


# process text from sefaria and create dictionary by parshiot for the english text
def createHebParshiot():
    return _createParshiot(VERSION_TITLE_HEB)


# helper method for parsha dictionary creation
def _createParshiot(version):
    # connect to the db server
    client = MongoClient()
    db = client.sefaria

    # code from Prof. Joshua Waxman
    parshiot = db.parshiot
    p = OrderedDict()
    stop_list = "Yom Sukkot Pesach Rosh Shabbat Atzeret Shavuot -".split()
    for parsha in parshiot.find():
        name = parsha['parasha']
        if not any(word in name for word in stop_list) or name == "Lech-Lecha":
            ref = parsha['ref']
            sefer, span = ref.split()
            start, end = span.split('-')
            start_ch, start_v = start.split(':')
            if ':' in end:
                end_ch, end_v = end.split(':')
            else:
                end_ch = start_ch
                end_v = end
            p[name] = (sefer, int(start_ch), int(start_v), int(end_ch), int(end_v))


    # using the starting chapter and verse and ending chapter and verse, iterate through
    # the sefaria text and create dictonary 'parshiot' organized by parsha name as key
    parshiot = defaultdict()
    for parsha,t in p.items():
        sefer, start_ch, start_v, end_ch, end_v = t
        d = dict(versionTitle= version, title=sefer)

        # use full text of the sefer
        book = db.texts.find_one(d)

        # add the text of the first chapter starting from the appropriate pasuk
        text = book['chapter'][start_ch-1][start_v-1:]

        # add the full text from chapters between first and last
        for chapt in range(start_ch, end_ch-1):
            text+=book['chapter'][chapt]

        # add the text from the last chapter
        text += book['chapter'][end_ch-1][:end_v-1]
        parshiot[parsha] = text

    return parshiot


# return a tokenized parsha - a list of the parsha words
def splitParsha(parshaName, parshiot):
    list = []
    for i in parshiot[parshaName]:
        words = i.split(" ")
        for each in words: list.append(each)
    return(list)



# return dictionary of "tokenized" parshiot - each parsha as key with each word in parsha in a list as the value
def parshiotSplit(splitParshiot):
    for each in splitParshiot:
        splitParshiot[each] = splitParsha(each, splitParshiot)
    return splitParshiot


# strip the text down by letter frequency - only keeping the 2 most frequent letters in each hebrew word
def processWordByFrequency(word):
    frequencies = HebrewLetterFrequency.main()

    if len(word) == 1: return word

    # remove all ending letters
    for j in range(len(word)):
        if word[j] in HebrewLetterFrequency.endings.keys():
            word = word.replace(word[j], HebrewLetterFrequency.endings[word[j]])

    if (frequencies[word[0]]<frequencies[word[1]]):
        min1 = word[0] #smallest
        min2 = word[1]
    else:
        min1 = word[1]
        min2 = word[0]
    for i in range(2,len(word)):
        freq = frequencies[word[i]]
        if freq < frequencies[min2]:
            if freq < frequencies[min1]: # the current letter has the smallest frequency
                min2 = min1
                min1 = word[i]
            else: # the current letter has the second smallest frequency
                min2 = word[i]
    return min1+min2


# return the dictionary of parshiot and text, but with each word processed to 2 letter minimum frequency
# the words will still be maintained, so TF-IDF can be run and the same indeces can be used to return the full words
def processParshiotByFrequency():
    freqParshiot = parshiotSplit(createSplitParshiot())
    for parsha, value in freqParshiot.items():
        for i in range(len(value)): # for each word in the parsha
            value[i] = processWordByFrequency(value[i])
        freqParshiot[parsha] = value
    return freqParshiot


# return the tokenized parshiot dictionary - dictionary with parshiot as keys and lists of parsha words as values
def createSplitParshiot(lang='heb'):
    if lang == 'heb':
        parshiot = createHebParshiot()
    else:
        parshiot = createEngParshiot()
    splitParshiot = parshiotSplit(parshiot)
    return splitParshiot
















