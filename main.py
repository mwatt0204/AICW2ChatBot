# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import nltk
import requests
import json
import csv
import re
import googleplaces
import enum
import fuzzywuzzy

from googleplaces import GooglePlaces, types, lang
from nltk import word_tokenize, pos_tag
from nltk.chat.util import Chat
from spellchecker import SpellChecker
from fuzzywuzzy import fuzz

_messageCount = 0
_expectedResponse = None
_percentThresholdRatio = 95
_percentThresholdPartial = 90

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

months = {
    "jan": "01m",
    "january": "01m",
    "feb": "02m",
    "february": "02m",
    "march": "03m",
    "april": "04m",
    "apr": "04m",
    "may": "05m",
    "jun": "06m",
    "june": "06m",
    "july": "07m",
    "jul": "07m",
    "august": "08m",
    "aug": "08m",
    "september": "09m",
    "sep": "09m",
    "sept": "09m",
    "october": "10m",
    "oct": "10m",
    "november": "11m",
    "nov": "11m",
    "december": "12m",
    "dec": "dec",
}


numberCovserisonsForChoiceSelection = {
    "first": "1",
    "second": "2",
    "third": "3",
    "forth": "4",
    "first one": "1",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
}

class Journy:
    messagecounter = 0
    startlocation = None
    destinatinon = None
    depaturetdate = None
    returnNeeded = None
    returndate = None
    choices = []


_journy = Journy()

noise_list = ["is", "a", "this", "i", "me"]

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
    noise_free_words = [word for word in words if word.lower() not in noise_list]
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


def _lookup_months(input_text):
    words = input_text.split()
    new_words = []
    for word in words:
        if word.lower() in months:
            word = months[word.lower()]
        new_words.append(word)
        new_text = " ".join(new_words)
    return new_text


def _spellCheck(input_word):
    spell = SpellChecker()
    return spell.correction(input_word)


def _genoratePosTags(input_text):
    tokens = word_tokenize(input_text)
    return pos_tag(tokens)


def _FindDateInText(input_text):
    timeFramewords = ["tomorrow", "fortnight", "monday", "tuesday", "wednesday", "thursday", "friday",
                      "saturday", "sunday", "week", "month", "weekend"]

    dates = []
    # extreamly likely to be date and right
    # dates = dates + re.findall(r'\d+\S\d+\S\d+', input_text)
    dates = dates + _findtagsCD(input_text)
    # hgihly likely to be date

    # possilbe relevent dates
    tokens = word_tokenize(input_text)
    for token in tokens:
        if token.lower() in timeFramewords:
            dates = dates + [token]

    return dates


# testing perpopuse
def myfirstbot():
    print("hello lets go")
    chat = Chat(chat_responsies)
    chat.converse()


def _findSations(input_text):
    stations = []
    possiblePlaces = _findtagsNNP(input_text)
    for places in possiblePlaces:
        location = places + ', England'
        try:
            response = google_places.nearby_search(location=location, keyword='', radius=10000,
                                                   types=[types.TYPE_TRAIN_STATION])
            if response.places[0] != None:
                stations = stations + [response.places[0]]
        except:
            pass
    return stations


# https://drumcoder.co.uk/blog/2013/dec/23/finding-proper-nouns-nltk/
def _findtagsNNP(input_text):
    cosecutive = False
    nouns = []
    for word, pos in nltk.pos_tag(nltk.word_tokenize(input_text)):
        if pos == 'NNP' or pos == 'NNPS' or pos:
            if cosecutive:
                nouns[-1] = nouns[-1] + " " + word
            else:
                nouns.append(word)
            cosecutive = True
        else:
            cosecutive = False
    return nouns


def _findtagsNouns(input_text):
    cosecutive = False
    nouns = []
    for word, pos in nltk.pos_tag(nltk.word_tokenize(input_text)):
        if pos == 'NNP' or pos == 'NNPS' or pos == "NN":
            if cosecutive:
                nouns[-1] = nouns[-1] + " " + word
            else:
                nouns.append(word)
            cosecutive = True
        else:
            cosecutive = False
    return nouns


def _findSations2(input_text):
    nouns = _findtagsNouns(input_text)
    # tokens = nltk.word_tokenize(input_text)
    for noun in nouns:
        print(noun)
    return compareNounToStationList(nouns)


def compareNounToStationList(nouns):
    possibalStations = []
    with open("GB stations.csv") as stationList:
        reader = csv.reader(stationList)
        for noun in nouns:
            stationList.seek(0,0)
            print(noun)
            for row in reader:
                ratio = fuzz.ratio(noun.lower(), row[0].lower())
                if ratio >= _percentThresholdRatio:
                    print(noun + "," + row[0] + "," + str(ratio))
                    possibalStations = possibalStations + [row[0]]
        print(len(possibalStations))
        if len(possibalStations) == 0:
            for noun in nouns:
                count = 0
                stationList.seek(0, 0)
                print(noun)
                for row in reader:
                    ratio = fuzz.partial_ratio(noun.lower(), row[0].lower())
                    if ratio >= _percentThresholdPartial:
                        count = count + 1
                        print(noun + "," + row[0] + "," + str(ratio))
                        possibalStations = possibalStations + [row[0]]
                if count > 10:
                    for i in range(count):
                         del possibalStations[-1]

        return possibalStations


def _findtagsCD(input_text):
    cosecutive = False
    nouns = []
    for word, pos in nltk.pos_tag(nltk.word_tokenize(input_text)):
        if pos == 'CD':
            if cosecutive:
                nouns[-1] = nouns[-1] + " " + word
            else:

                nouns.append(word)
            cosecutive = True
        else:
            cosecutive = False
    return nouns



def _extractInformatoin(input_text):
    #if(len(_journy.choices) > 0):
     #   lieklychoices = _findtagsCD(input_text)
    input_text = _lookup_words(input_text)
    input_text = _lookup_months(input_text)
    keydates = _FindDateInText(input_text)
    keylocations = _findSations2(input_text)
    # keylocations = _findSations(input_text)
    return keylocations, keydates


def _moveConservationFowords():
    if _journy.destinatinon == None:
        return "where are you looking to traval to", 0
    if _journy.startlocation == None:
        return "could you tell me where you are setting off from", 1
    if _journy.depaturetdate == None:
        return "what date are you looking to traval", 2
    if _journy.returnNeeded == None:
        return "would you like return", 3


def _populateJournyLocatoins(locations):
    if _expectedResponse == 0:
        if len(locations) == 1:
            _journy.destinatinon = locations[0]
            return True
    elif _expectedResponse == 1:
        if len(locations) == 1:
            _journy.startlocation = locations[0]
            return True
    else:
        return False


def _populateJournyDates(dates):
    if _expectedResponse == 2:
        if len(dates) == 1:
            _journy.depaturetdate = dates[0]
            return True
    else:
        return False


def _getOptions(locations):
    if len(locations) < 5:
        _journy.choices = locations
        message = "i found " + str(len(locations)) + " liekly mataches did you mean any of these: \n"
        for i in range(len(locations)):
            message = message + str(i) + "." + locations[i] + ". \n"
    else:
        message = " if you tried to give a locations it might have been a bit vague please try be more persfice and check spellings"
    return message,


def _messagerecived(input_text):
    global _messageCount
    global _expectedResponse
    _messageCount = _messageCount + 1
    response = ""
    input_text = _remove_noise(input_text)
    locations, dates = _extractInformatoin(input_text)
    daterecived = False
    if len(locations) == 1:
        daterecived = _populateJournyLocatoins(locations)
    if len(dates) == 1:
        daterecived = _populateJournyDates(dates)
    if daterecived or _messageCount == 1:
        word, _expectedResponse = _moveConservationFowords()
    elif (len(locations) > 1):
        word = _getOptions(locations)
    else:
        word = "i don't konw hat you mean"
        temp,_expectedResponse = _moveConservationFowords()
        word = word + temp

    print("Destination: " + str(_journy.destinatinon))
    print("StartLocatin: " + str(_journy.startlocation))
    print("Depaturea Date: " + str(_journy.depaturetdate))

    if _messageCount == 1:
        response = "Hello my Name is Thomas the train bot: an automated ai chatbot than can help you find train traval times" + "\n" + word
    else:
        response = word
    return response


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # response = google_places.nearby_search(location='norwich, England', keyword='TrainStation', radius=20000,
    #                                        types=[types.TYPE_TRAIN_STATION])

    while True:
        message = str(input())
        # print(_genoratePosTags(message))
        # print(_findSations2(message))
        print(_messagerecived(message))

#   satations = _messagerecived("hello there im looking to book a train Jan")
#  print(satations)
#
#   satations = _messagerecived("tomowrow would be best going to London 12/11/2020  from Norwich")
#  print(satations)
