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
import params
from TwitterSearch import *


# DEFINES
OUTFILE = 'test.html'
#see params.py
keywords = ['apple', 'iphone', 'ios', 'aapl']

#keywords = {'apple', 'aapl', 'tim cook', 'iphone', 'steve jobs', 'cupertino', 'wwdc', 'macbook',
#            'ipod', 'itunes', 'ipad', 'macos', 'snow leopard', 'mountain lion', 'ios', 'xcode',
#            'facetime', 'appstore', 'osx', 'nsobject'}


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


def getTweetsForKeyword(keyword):
    """
    Get the (recent) tweets for a given keyword
    :param keyword: the query keyword
    :return: a list of tweets. List is empty if an error occurs
    """
    tweet_list = []

    try:
        print '*** Searching tweets for keyword:', keyword, ' ...'
        tso = TwitterSearchOrder()
        tso.setKeywords([keyword])
        tso.setLanguage('en')
        tso.setResultType('recent')
        tso.setCount(10)
        tso.setIncludeEntities(True)

        ts = TwitterSearch(
            consumer_key=params.CONSUMER_KEY,
            consumer_secret=params.CONSUMER_SECRET,
            access_token=params.ACCESS_TOKEN,
            access_token_secret=params.ACCESS_TOKEN_SECRET
        )

        ts.authenticate()

        counter = 0

        for tweet in ts.searchTweetsIterable(tso):
            counter += 1
            tweet_list.append(tweet)
        print '*** Found a total of %i tweets for keyword:' % counter, keyword
        return tweet_list

    except TwitterSearchException, e:
        print "[ERROR]", e.message
        return tweet_list


def extractLocation(tweet):
    try:
        location = tweet["place"]["country_code"]
    except:
        location = "unknown"
    return location


if __name__ == '__main__':

    counter = {}

    for keyword in keywords:

        tweet_list = getTweetsForKeyword(keyword)

        for tweet in tweet_list:
            country = extractLocation(tweet)

            if country != "unknown":

                clean_text = normalize_tweet(tweet["text"])
                pos_score, neg_score = senti_classifier.polarity_scores([clean_text])
                if pos_score > neg_score:
                    vote = 1
                elif pos_score < neg_score:
                    vote = -1
                else:
                    vote = 0

                try:
                    counter[country] += vote
                except KeyError:
                    counter[country] = vote

    htmllist = []

    for country, sentiment in counter.iteritems():
        htmllist.append(([country, sentiment]))

    array_to_html_page(htmllist, OUTFILE)
    print "Check out the " + OUTFILE + " file"



    #TODO:
    #implement new twitter 1.1 (library :)
    #sqlite storage of tweets
    #classify with tweet data, not movie!