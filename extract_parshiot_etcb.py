# jw
# sept 10, 2019
from pymongo import MongoClient
from collections import OrderedDict, defaultdict

f = open("shorashim.torah.out.txt", 'r', encoding='utf-8')
pasuk_dict = dict()
for line in f:
    reference, data = line.split(':')
    pasuk_dict[reference] = eval(data)
f.close()

def createParshiot():
    # connect to the db server
    client = MongoClient()
    db = client.sefaria

    parshiot = db.parshiot
    p = OrderedDict()
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
    parsha_text = dict()
    for parsha, t in p.items():
        print(parsha)
        sefer, start_ch, start_v, end_ch, end_v = t
        # iterate through first chapter
        for verse in range(start_v, 1000):
            ref = sefer + ' ' + str(start_ch) + ' ' + str(verse)
            if ref in pasuk_dict:
                text += [root for _, root in pasuk_dict[ref]]
            else: # out of pesukim
                break

        # handle middle chapters
        for chapter in range(start_ch+1, end_ch):
            for verse in range(1, end_v+1):
                ref = sefer + ' ' + str(chapter) + ' ' + str(verse)
                if ref in pasuk_dict:
                    text += [root for _, root in pasuk_dict[ref]]
                else:  # out of pesukim
                    break

        # handle last chapter
        if start_ch < end_ch:
            for verse in range(1, 1000):
                ref = sefer + ' ' + str(end_ch) + ' ' + str(verse)
                if ref in pasuk_dict:
                    text += [root for _, root in pasuk_dict[ref]]
                else:  # out of pesukim
                    break

        parsha_text[parsha] = text
        text = []
        #break

    pnames = ["Bereshit", "Noach", "Lech-Lecha", "Vayera", "Chayei Sara", "Toldot", "Vayetzei", "Vayishlach", "Vayeshev", "Miketz", "Vayigash", "Vayechi", "Shemot", "Vaera", "Bo", "Beshalach", "Yitro", "Mishpatim", "Terumah", "Tetzaveh", "Ki Tisa", "Vayakhel", "Pekudei", "Vayikra", "Tzav", "Shmini", "Tazria", "Metzora", "Achrei Mot", "Kedoshim", "Emor", "Behar", "Bechukotai", "Bamidbar", "Nasso", "Beha'alotcha", "Sh'lach", "Korach", "Chukat", "Balak", "Pinchas", "Matot", "Masei", "Devarim", "Vaetchanan", "Eikev", "Re'eh", "Shoftim", "Ki Teitzei", "Ki Tavo", "Nitzavim", "Vayeilech", "Ha'Azinu", "VeZot HaBeracha"]
    f = open('parshiot.txt', 'w', encoding='utf-8')
    for name in pnames:
        print(' '.join(parsha_text[name]), file=f)
    f.close()

from sklearn.feature_extraction.text import TfidfVectorizer
def gather_tf_idf():
   f = open('parshiot.txt', 'r', encoding='utf-8')
   docs = [line for line in f]
   f.close()

   vectorizer = TfidfVectorizer(analyzer="word",token_pattern="[\S]+")
   X = vectorizer.fit_transform(docs)
   vocab_lookup = {v: k for k, v in vectorizer.vocabulary_.items()}
   vocab_lookup2 = {k: v for k, v in vectorizer.vocabulary_.items()}

   feature_names = vectorizer.get_feature_names()

   doc = 0
   feature_index = X[doc, :].nonzero()[1]
   tfidf_scores = zip(feature_index, [X[doc, x] for x in feature_index])

   d = {}
   for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
       d[w] = s

# step 1: create the parshiot.txt, helpful for tf-idf
# comment out if you already have parshiot.txt
createParshiot()

#step 2: get the tf_idf scores for all words in all documents
gather_tf_idf()


