"""As described by Shmidman, Koppel, and Porat (https://arxiv.org/ftp/arxiv/papers/1602/1602.08715.pdf), hebrew words
 can be more effectively analyzed here by comparing the root letters of various words. Their algorithm finds the most
 infrequent hebrew letters in the given corpus and then, when analyzing any given word, only look at the 2 most
 infrequent letters. This can allow for more effective finding of "significant words", as the repetition of nearly
 identical words can be found. """

from pymongo import MongoClient
from collections import OrderedDict, defaultdict, Counter

# version of the text being used
VERSION_TITLE = "Tanach with Text Only"

# connect to the db server
client = MongoClient()
db = client.sefaria

full_text = db.texts.find(dict(versionTitle=VERSION_TITLE))
hebrew_chars = list("אבגדהוזחטיכךלמםנןסעפףצץקרשת")
char_count = Counter(hebrew_chars)
i = 0

# iterate through all letters of the hebrew tanakh, and return a counter with the frequency for each letter
for book in full_text:
    text = book['chapter']
    for chapter in text:
        words = [list(word) for word in chapter]
        all_chars_in_chapter = [list(char) for char in words]
        for char_list in all_chars_in_chapter:
            for each in hebrew_chars:
                char_count[each]+= char_list.count(each)

# char_count['כ'] += char_count['ך']
# char_count['נ'] += char_count['ן']
# char_count['צ'] += char_count['ץ']
# char_count['מ'] += char_count['ם']
# char_count['פ'] += char_count['ף']



endings = dict(zip('ם ץ ן ך ף'.split(), 'מ צ נ כ פ'.split()))

# equate the count for ending letters
for endChar, normalChar in endings.items():
    char_count[normalChar] += char_count[endChar]

# remove superfluous counts of ending letters
for char in endings.keys(): del char_count[char]



def main():
    return char_count

