# jw
# sept 10, 2019
from pymongo import MongoClient
from collections import OrderedDict, defaultdict
from pprint import pprint
from csv import writer

f = open("shorashim.torah.out.txt", 'r', encoding='utf-8')
pasuk_dict = dict()
for line in f:
    reference, data = line.split(':')
    pasuk_dict[reference] = eval(data)
f.close()

p = OrderedDict()
parsha_text = dict()
parsha_refs = dict()

romanization = None
def unromanize(shoresh: str) -> str:
    global romanization
    if romanization is None: # load the first time
        fin = open("romanization.txt", encoding='utf-8')
        romanization = {}
        for line in fin:
            enLetter, heLetter = line.strip().split("\t")
            romanization[enLetter] = heLetter
        fin.close()

    hebrew = ""
    for letter in shoresh:
        if letter in romanization:
            hebrew += romanization[letter]
    return hebrew


def createParshiot():
    # connect to the db server
    client = MongoClient()
    db = client.sefaria

    parshiot = db.parshiot
    stop_list = "Yom Sukkot Pesach Rosh Shabbat Atzeret Shavuot -".split()
    for parsha in parshiot.find():
        name = parsha['parasha']
        if not any(word in name for word in stop_list) or name == "Lech-Lecha" or name == '':
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

    p["VeZot HaBeracha"] = ('Deuteronomy', 33, 1, 34, 29)
    # using the starting chapter and verse and ending chapter and verse, iterate through
    # and use it to look up in the ETCB dataset
    text = []
    refs = []

    for parsha, t in p.items():
        print(parsha)
        sefer, start_ch, start_v, end_ch, end_v = t
        # iterate through first chapter
        for verse in range(start_v, 1000):
            ref = sefer + ' ' + str(start_ch) + ' ' + str(verse)
            if ref in pasuk_dict:
                text += [root for _, root in pasuk_dict[ref]] + [':']
                refs.append(ref)
            else: # out of pesukim
                break

        # handle middle chapters
        for chapter in range(start_ch+1, end_ch):
            for verse in range(1, 1000):
                ref = sefer + ' ' + str(chapter) + ' ' + str(verse)
                if ref in pasuk_dict:
                    text += [root for _, root in pasuk_dict[ref]] + [':']
                    refs.append(ref)
                else:  # out of pesukim
                    break

        # handle last chapter
        if start_ch < end_ch:
            for verse in range(1, 1000):
                ref = sefer + ' ' + str(end_ch) + ' ' + str(verse)
                if ref in pasuk_dict:
                    text += [root for _, root in pasuk_dict[ref]] + [':']
                    refs.append(ref)
                else:  # out of pesukim
                    break

        parsha_text[parsha] = ' '.join(text)
        parsha_refs[parsha] = refs
        text = []
        refs = []
        #break

    pnames = ["Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi", "Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav", "Shmini", "Tazria", "Metzora", "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai", "Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach", "Chukat", "Balak", "Pinchas", "Matot", "Masei", "Devarim", "Vaetchanan", "Eikev", "Re'eh", "Shoftim", "Ki Teitzei", "Ki Tavo", "Nitzavim", "Vayeilech", "Ha'Azinu", "VeZot HaBeracha"]
    f = open('parshiot.txt', 'w', encoding='utf-8')
    for name in pnames:
        print(parsha_text[name], file=f)
    f.close()

from sklearn.feature_extraction.text import TfidfVectorizer
tf_parsha = {}
def gather_tf_idf():
   f = open('parshiot.txt', 'r', encoding='utf-8')
   docs = []
   for line in f:
       line = line.replace(' : ', ' ')
       docs.append(line)
   f.close()

   vectorizer = TfidfVectorizer(analyzer="word",token_pattern="[\S]+")
   X = vectorizer.fit_transform(docs)
   vocab_lookup = {v: k for k, v in vectorizer.vocabulary_.items()}
   vocab_lookup2 = {k: v for k, v in vectorizer.vocabulary_.items()}

   feature_names = vectorizer.get_feature_names()
   pnames = ["Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev",
             "Miketz", "Vayigash", "Vayechi", "Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah",
             "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav", "Shmini", "Tazria", "Metzora",
             "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai", "Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach",
             "Korach", "Chukat", "Balak", "Pinchas", "Matot", "Masei", "Devarim", "Vaetchanan", "Eikev", "Re'eh",
             "Shoftim", "Ki Teitzei", "Ki Tavo", "Nitzavim", "Vayeilech", "Ha'Azinu", "VeZot HaBeracha"]

   for doc, name in enumerate(pnames):
       feature_index = X[doc, :].nonzero()[1]
       tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])

       d = {}
       for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
           d[w] = s

       tf_parsha[name] = d

   pprint(tf_parsha)

def find_leitworte():
    pnames = ["Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach",
              "Vayeshev",
              "Miketz", "Vayigash", "Vayechi", "Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah",
              "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav", "Shmini", "Tazria", "Metzora",
              "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai", "Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach",
              "Korach", "Chukat", "Balak", "Pinchas", "Matot", "Masei", "Devarim", "Vaetchanan", "Eikev", "Re'eh",
              "Shoftim", "Ki Teitzei", "Ki Tavo", "Nitzavim", "Vayeilech", "Ha'Azinu", "VeZot HaBeracha"]

    VERSE_WINDOW = 60
    REPETITION = 3

    f = open('leitworte.' + str(VERSE_WINDOW) + '.' + str(REPETITION) + '.csv', 'w', encoding='utf-8', newline='')
    csv_writer = writer(f)

    csv_writer.writerow('start_ref,end_ref,span,half_span_length,heb,repetitions,tfidf'.split(','))

    for parsha in pnames:
        verses = parsha_text[parsha].split(' : ')
        refs = parsha_refs[parsha]
        word_occurrences = defaultdict(list)

        # first pass. just calculate bagOfWords for each verse
        bagOfWordsVerses = []
        for verse in verses:
            bagOfWordsCurrent = defaultdict(int)
            words = verse.split()
            for word in words: # start with unigrams
                bagOfWordsCurrent[word] += 1
            bagOfWordsVerses.append(bagOfWordsCurrent)

        bagOfWordsSpan = defaultdict(int)
        bagOfWordsCurrent = defaultdict(int)
        bagOfWordsQueue = []
        refQueue = []
        n = len(verses)
        for i, (verse, ref, bow) in enumerate(zip(verses, refs, bagOfWordsVerses), 1):
            # on removal, check if after span comes into scope, it works as Leitwort
            last_verse = (i == n)
            if (len(bagOfWordsQueue) == VERSE_WINDOW or last_verse) and len(bagOfWordsQueue) > 0:
                for word, count in bagOfWordsSpan.items():
                    if count % REPETITION == 0 and (last_verse or (word not in bagOfWordsCurrent and word in bagOfWordsQueue[0])):
                        r = word_occurrences[word][0]
                        r2 = word_occurrences[word][-1]
                        lower_word = word.lower()
                        tfidf = tf_parsha[parsha][lower_word]
                        heb = unromanize(word)

                        # check that this Leitwort actually occurs in an island
                        # that is, (1) first get the gap between first and last verse
                        # to acquire the true span, different from the window
                        start = refs.index(r)
                        end = refs.index(r2)
                        span = end - start + 1
                        half_span = span // 4
                        prior_window = start - half_span
                        prior_window = max(prior_window, 0)
                        follow_window = end + half_span
                        follow_window = min(follow_window, n-1)

                        # then, (2) take half that window and make sure that the
                        # Leitwort doesn't occur in that half-span of verses before
                        # and after
                        found = False

                        for i in range(prior_window, start):
                            if word in bagOfWordsVerses[i].keys():
                                found = True
                        for i in range(end + 1, follow_window):
                            if word in bagOfWordsVerses[i].keys():
                                found = True

                        if not found:
                            print(r, '-', r2, heb, "occurred", count, "times with tf-idf of", tfidf)
                            csv_writer.writerow([r, r2, span, half_span, heb, count, tfidf])

                refQueue.pop(0)
                # time to shift off the first item
                # maybe should use the fast one from
                # collections to speed this up
                p = bagOfWordsQueue.pop(0)
                # remove each word from span
                for word, count in p.items():
                    bagOfWordsSpan[word] -= count

                    if bagOfWordsSpan[word] == 0:
                        del bagOfWordsSpan[word]

                    word_occurrences[word].pop(0)

            for word, count in bow.items(): # start with unigrams
                bagOfWordsSpan[word] += count

                if word_occurrences[word] == [] or word_occurrences[word][-1] != ref:
                    word_occurrences[word].append(ref)

            bagOfWordsQueue.append(bow)
            refQueue.append(ref)
    f.close()

# step 1: create the parshiot.txt, helpful for tf-idf
# comment out if you already have parshiot.txt
createParshiot()

#step 2: get the tf_idf scores for all words in all documents
gather_tf_idf()

# step 3: find leitworte, for each parasha, moving thru window of verses
find_leitworte()
