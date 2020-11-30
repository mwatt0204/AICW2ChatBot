# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import nltk
import requests
import json
import csv
import re
import googleplaces

from googleplaces import GooglePlaces, types, lang
from nltk import word_tokenize, pos_tag
from nltk.chat.util import Chat
from spellchecker import SpellChecker

_API_KEY = ''
google_places = GooglePlaces(_API_KEY)

abbreviations = {
    "$": " dollar ",
    "€": " euro ",
    "4ao": "for adults only",
    "a.m": "before midday",
    "a3": "anytime anywhere anyplace",
    "aamof": "as a matter of fact",
    "acct": "account",
    "adih": "another day in hell",
    "afaic": "as far as i am concerned",
    "afaict": "as far as i can tell",
    "afaik": "as far as i know",
    "afair": "as far as i remember",
    "afk": "away from keyboard",
    "app": "application",
    "approx": "approximately",
    "apps": "applications",
    "asap": "as soon as possible",
    "asl": "age, sex, location",
    "atk": "at the keyboard",
    "ave.": "avenue",
    "aymm": "are you my mother",
    "ayor": "at your own risk",
    "b&b": "bed and breakfast",
    "b+b": "bed and breakfast",
    "b.c": "before christ",
    "b2b": "business to business",
    "b2c": "business to customer",
    "b4": "before",
    "b4n": "bye for now",
    "b@u": "back at you",
    "bae": "before anyone else",
    "bak": "back at keyboard",
    "bbbg": "bye bye be good",
    "bbc": "british broadcasting corporation",
    "bbias": "be back in a second",
    "bbl": "be back later",
    "bbs": "be back soon",
    "be4": "before",
    "bfn": "bye for now",
    "blvd": "boulevard",
    "bout": "about",
    "brb": "be right back",
    "bros": "brothers",
    "brt": "be right there",
    "bsaaw": "big smile and a wink",
    "btw": "by the way",
    "bwl": "bursting with laughter",
    "c/o": "care of",
    "cet": "central european time",
    "cf": "compare",
    "cia": "central intelligence agency",
    "csl": "can not stop laughing",
    "cu": "see you",
    "cul8r": "see you later",
    "cv": "curriculum vitae",
    "cwot": "complete waste of time",
    "cya": "see you",
    "cyt": "see you tomorrow",
    "dae": "does anyone else",
    "dbmib": "do not bother me i am busy",
    "diy": "do it yourself",
    "dm": "direct message",
    "dwh": "during work hours",
    "e123": "easy as one two three",
    "eet": "eastern european time",
    "eg": "example",
    "embm": "early morning business meeting",
    "encl": "enclosed",
    "encl.": "enclosed",
    "etc": "and so on",
    "faq": "frequently asked questions",
    "fawc": "for anyone who cares",
    "fb": "facebook",
    "fc": "fingers crossed",
    "fig": "figure",
    "fimh": "forever in my heart",
    "ft.": "feet",
    "ft": "featuring",
    "ftl": "for the loss",
    "ftw": "for the win",
    "fwiw": "for what it is worth",
    "fyi": "for your information",
    "g9": "genius",
    "gahoy": "get a hold of yourself",
    "gal": "get a life",
    "gcse": "general certificate of secondary education",
    "gfn": "gone for now",
    "gg": "good game",
    "gl": "good luck",
    "glhf": "good luck have fun",
    "gmt": "greenwich mean time",
    "gmta": "great minds think alike",
    "gn": "good night",
    "g.o.a.t": "greatest of all time",
    "goat": "greatest of all time",
    "goi": "get over it",
    "gps": "global positioning system",
    "gr8": "great",
    "gratz": "congratulations",
    "gyal": "girl",
    "h&c": "hot and cold",
    "hp": "horsepower",
    "hr": "hour",
    "hrh": "his royal highness",
    "ht": "height",
    "ibrb": "i will be right back",
    "ic": "i see",
    "icq": "i seek you",
    "icymi": "in case you missed it",
    "idc": "i do not care",
    "idgadf": "i do not give a damn fuck",
    "idgaf": "i do not give a fuck",
    "idk": "i do not know",
    "ie": "that is",
    "i.e": "that is",
    "ifyp": "i feel your pain",
    "IG": "instagram",
    "iirc": "if i remember correctly",
    "ilu": "i love you",
    "ily": "i love you",
    "imho": "in my humble opinion",
    "imo": "in my opinion",
    "imu": "i miss you",
    "iow": "in other words",
    "irl": "in real life",
    "j4f": "just for fun",
    "jic": "just in case",
    "jk": "just kidding",
    "jsyk": "just so you know",
    "l8r": "later",
    "lb": "pound",
    "lbs": "pounds",
    "ldr": "long distance relationship",
    "lmao": "laugh my ass off",
    "lmfao": "laugh my fucking ass off",
    "lol": "laughing out loud",
    "ltd": "limited",
    "ltns": "long time no see",
    "m8": "mate",
    "mf": "motherfucker",
    "mfs": "motherfuckers",
    "mfw": "my face when",
    "mofo": "motherfucker",
    "mph": "miles per hour",
    "mr": "mister",
    "mrw": "my reaction when",
    "ms": "miss",
    "mte": "my thoughts exactly",
    "nagi": "not a good idea",
    "nbc": "national broadcasting company",
    "nbd": "not big deal",
    "nfs": "not for sale",
    "ngl": "not going to lie",
    "nhs": "national health service",
    "nrn": "no reply necessary",
    "nsfl": "not safe for life",
    "nsfw": "not safe for work",
    "nth": "nice to have",
    "nvr": "never",
    "nyc": "new york city",
    "oc": "original content",
    "og": "original",
    "ohp": "overhead projector",
    "oic": "oh i see",
    "omdb": "over my dead body",
    "omg": "oh my god",
    "omw": "on my way",
    "p.a": "per annum",
    "p.m": "after midday",
    "pm": "prime minister",
    "poc": "people of color",
    "pov": "point of view",
    "pp": "pages",
    "ppl": "people",
    "prw": "parents are watching",
    "ps": "postscript",
    "pt": "point",
    "ptb": "please text back",
    "pto": "please turn over",
    "qpsa": "what happens",  # "que pasa",
    "ratchet": "rude",
    "rbtl": "read between the lines",
    "rlrt": "real life retweet",
    "rofl": "rolling on the floor laughing",
    "roflol": "rolling on the floor laughing out loud",
    "rotflmao": "rolling on the floor laughing my ass off",
    "rt": "retweet",
    "ruok": "are you ok",
    "sfw": "safe for work",
    "sk8": "skate",
    "smh": "shake my head",
    "sq": "square",
    "srsly": "seriously",
    "ssdd": "same stuff different day",
    "tbh": "to be honest",
    "tbs": "tablespooful",
    "tbsp": "tablespooful",
    "tfw": "that feeling when",
    "thks": "thank you",
    "tho": "though",
    "thx": "thank you",
    "tia": "thanks in advance",
    "til": "today i learned",
    "tl;dr": "too long i did not read",
    "tldr": "too long i did not read",
    "tmb": "tweet me back",
    "tntl": "trying not to laugh",
    "ttyl": "talk to you later",
    "u": "you",
    "u2": "you too",
    "u4e": "yours for ever",
    "utc": "coordinated universal time",
    "w/": "with",
    "w/o": "without",
    "w8": "wait",
    "wassup": "what is up",
    "wb": "welcome back",
    "wtf": "what the fuck",
    "wtg": "way to go",
    "wtpa": "where the party at",
    "wuf": "where are you from",
    "wuzup": "what is up",
    "wywh": "wish you were here",
    "yd": "yard",
    "ygtr": "you got that right",
    "ynk": "you never know",
    "zzz": "sleeping bored and tired"
}

noise_list = ["is", "a", "this", "..."]

words = ["item", "cat", "dog"]

chat_responsies = [
    [
        r"hi|hey|hello",
        ["hello", "greatings", "hello there"]
    ],
    [
        r"(.*) (language) (.*) ?",
        ["I am written in python but I speak English.", ]
    ],
]


def search_places_by_coordinate(self, location, radius, types):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': radius,
        'types': types,
        'key': self.apiKey
    }
    res = requests.get(endpoint_url, params=params)
    results = json.loads(res.content)
    return results


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def _remove_noise(input_text):
    words = input_text.split()
    noise_free_words = [word for word in words if word not in noise_list]
    noise_free_text = " ".join(noise_free_words)
    return noise_free_text


def _lookup_words(input_text):
    words = input_text.split()
    new_words = []
    for word in words:
        if word.lower() in abbreviations:
            word = abbreviations[word.lower()]
        new_words.append(word)
        new_text = " ".join(new_words)
    return new_text


# dosnt work
def _containesStations(input_text):
    words = input_text.split()
    new_words = []
    with open('station_codes (06-08-2020).csv', 'rt') as stationList:
        reader = csv.reader(stationList)
        locatoins = []
        stationList = csv.slit

        for row in reader:
            for item in row:
                if item.lower() in input_text.lower():
                    locatoins.append(item)
        return locatoins


def _spellCheck(input_word):
    spell = SpellChecker()
    return spell.correction(input_word)


def _genoratePosTags(input_text):
    tokens = word_tokenize(input_text)
    return pos_tag(tokens)


def _FindDateInText(input_text):
    timeFramewords = ["tomorrow", "yesterday", "fortnight", "monday", "tuesday", "wednesday", "thursday", "friday",
                      "saturday", "sunday", "week", "month"]

    dates = []
    # extreamly likely to be date and right
    dates = dates + re.findall(r'\d+\S\d+\S\d+', input_text)

    # hgihly likely to be date
    dates = dates + re.findall(r'[a-z]\w+\s\d+', input_text)

    # possilbe relevent dates
    tokens = word_tokenize(input_text)
    for token in tokens:
        if token in timeFramewords:
            dates = dates + [token]

    return dates


# testing perpopuse
def myfirstbot():
    print("hello lets go")
    chat = Chat(chat_responsies)
    chat.converse()


def _findSations(input_text):
    stations = []
    possiblePlaces = _findtags(input_text)
    for places in possiblePlaces:
        location = places + ', England'
        try:
            response = google_places.nearby_search(location=location, keyword='TrainStation', radius=10000,
                                                   types=[types.TYPE_TRAIN_STATION])
            if response.places[0] != None:
                stations = stations + [response.places[0]]
        except:
            pass
    return stations


# https://drumcoder.co.uk/blog/2013/dec/23/finding-proper-nouns-nltk/
def _findtags(input_text):
    cosecutive = False
    nouns = []
    for word, pos in nltk.pos_tag(nltk.word_tokenize(input_text)):
        if pos == 'NNP' or pos == 'NNPS':
            if cosecutive:
                nouns[-1] = nouns[-1] + " " + word
            else:
                nouns.append(word)
            cosecutive = True
        else:
            cosecutive = False
    return nouns


def _messagerecived(input_text):
    keyInformation = []
    keyInformation = keyInformation + _FindDateInText(input_text)
    keyInformation = keyInformation + _findSations(input_text)
    return keyInformation


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # response = google_places.nearby_search(location='norwich, England', keyword='TrainStation', radius=20000,
    #                                        types=[types.TYPE_TRAIN_STATION])

    satations = _messagerecived("i want a train to Great Yarmouth on the 12/12/2020 from Norwich and to return Jan 4th")
    print(satations)

    #    for place in response.places:
    #       print(place.name)
    #      print(place.geo_location)
    #     print(place.place_id)

print_hi('PyCharm')

#    nltk.download("all")

# Sample code to remove noisy words from a text
# myfirstbot()

nouns = _findtags("London Ringwood dad mum chair we are going to go very fun word  not sure monitor")
print(nouns)

print(_lookup_words("RT this is a retweeted tweet by u Shivam Bansal"))
print(_remove_noise("this is a sample text?"))
print(_spellCheck("instell"))
print(_genoratePosTags("I am going to fetch my cat from the shelter later and book it to the accounts"))
print(_genoratePosTags("five seven 6 9 July"))

print(_FindDateInText(
    "i want a train station tickent from 15/1/20 to 15-2-25   or maybe Jan 2nd  kjklfjkl 3   yesterday or tomorrow"))

# print(_containesStations("Bromley Cross"))
# print(_containesStations(" d  Abbey Wood"))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
