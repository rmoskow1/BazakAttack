"""Create a 2D array of text organized by Parsha and verse. i.e parshiot['Chayei Sarah'][0] returns
the first verse in the Parsha: Chayei Sarah from the Sefaria database text"""

from pymongo import MongoClient
from collections import OrderedDict, defaultdict
import math
import copy
from BazakAttack import HebrewLetterFrequency

# version of the text being used
VERSION_TITLE = "The Holy Scriptures: A New Translation (JPS 1917)"

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
    d = dict(versionTitle= VERSION_TITLE, title=sefer)

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


print(parshiot['Chayei Sara'])
splitParshiot = copy.deepcopy(parshiot)
