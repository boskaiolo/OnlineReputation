import re
import urllib
import json
import nltk
from nltk.corpus import stopwords
from senti_classifier import senti_classifier

# DEFINE
PAGES_TO_SCAN = 50

keywords = {'apple', 'aapl', 'tim cook', 'iphone', 'steve jobs', 'cupertino', 'wwdc', 'macbook',
            'ipod', 'itunes', 'ipad', 'macos', 'snow leopard', 'mountain lion', 'ios', 'xcode',
            'facetime', 'appstore', 'osx', 'nsobject'}
tweets = []


def normalize_tweet(text):

    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)

    text = text.lower()



    clean_text = ""

    for word in text.split():
        if word not in stopwords.words('english'):
            if word.startswith("@"):
                word = "*ACCOUNT*"
            elif word.startswith("http://"):
                word = "*LINK*"
            elif word.find("$") >= 0:
                word = ""
            elif len(word) < 3:
                word = ""
            else:
                word = pattern.sub(r"\1\1\1", word)
                #word = nltk.PorterStemmer().stem(word)

            clean_text = clean_text + " " + word

    return clean_text


if __name__ == '__main__':

    for word in keywords:

        for i in range(PAGES_TO_SCAN):
            page = i + 1
            response = urllib.urlopen("http://search.twitter.com/search.json?q=" + word + "&page=" + str(page))
            js = json.load(response)

            try:
                tweet_list = js["results"]

            except KeyError as e:
                continue

            for text in tweet_list:
                if "geo" in text.keys() and text["geo"] is not None:

                    coordinates = text["geo"]["coordinates"]
                    if coordinates[0] != 0.0 and coordinates[1] != 0.0:

                        clean_text = normalize_tweet(text["text"])

                        pos_score, neg_score = senti_classifier.polarity_scores([clean_text])
                        if pos_score > neg_score:
                            vote = 1
                        elif pos_score < neg_score:
                            vote = -1
                        else:
                            vote = 0

                        print coordinates[0], coordinates[1], vote






    print len(tweets)

    for t in tweets:
        print t




