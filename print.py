__author__ = "Alberto Boschetti"
__status__ = "Prototype"

import re
import urllib
import json
import nltk
from nltk.corpus import stopwords
import time
from senti_classifier import senti_classifier
from makehtml import array_to_html_page


# DEFINE
PAGES_TO_SCAN = 1
SLEEP_INTERVAL_FOR_GOOGLE_QUERY = 3


#keywords = {'apple', 'aapl', 'tim cook', 'iphone', 'steve jobs', 'cupertino', 'wwdc', 'macbook',
#            'ipod', 'itunes', 'ipad', 'macos', 'snow leopard', 'mountain lion', 'ios', 'xcode',
#            'facetime', 'appstore', 'osx', 'nsobject'}
keywords = {'apple', 'aapl', 'tim cook', 'iphone', 'steve jobs'}
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
                        tweets.append((coordinates[0], coordinates[1], vote,))

    counter = {}

    for t in tweets:
        response = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(t[0]) + "," + str(t[1]) + "&sensor=false")
        js = json.load(response)
        print js
        time.sleep(SLEEP_INTERVAL_FOR_GOOGLE_QUERY)

        try:
            res = js["results"]

        except:
            continue

        try:
            country = res[len(res) - 1]["formatted_address"]
        except:
            print "something wrong"
            continue


        try:
            counter[country] += t[2]

        except KeyError:
            counter[country] = t[2]


    print counter

    htmllist = []

    for key, value in counter.iteritems():
        temp = [key.decode("utf-8"),value]
        htmllist.append((temp))

    print htmllist
    print "put that list in the sample.html file :) then open it"

    array_to_html_page(htmllist, 'test.html')







