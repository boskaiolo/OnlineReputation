__author__ = "Alberto Boschetti"
__status__ = "Prototype"

import re
import random

from nltk.corpus import stopwords
from senti_classifier import senti_classifier
from TwitterSearch import *
from dateutil import parser

import params
from DbConnector import DBConnector
from makehtml import *
from other_libs import Namer
import string




# DEFINES

keywords = ['apple', 'iphone', 'ios', 'aapl']
#keywords = ['microsoft', 'sharepoint', 'windows8', 'msft']


def removeNonAscii(s):
    return "".join(i for i in s if ord(i) < 128)


def write_it(gender, twitter_use, popularity, keywords):
    sentiment_score = db.getSentimentWithFilter(gender, twitter_use, popularity, keywords)
    htmllist = []
    for entry in sentiment_score:
        htmllist.append(([entry[0], entry[1]]))
    array_to_html_page(htmllist, company+"-"+gender+"-"+str(twitter_use)+"-"+str(popularity))



def normalize_tweet(text):
    """
    Clean the tweet before sentiment analysis. Remove cashtags, links and account names. Transform hashtags in words
    :param text: the body of a tweet
    :return: a clean version of the body
    """
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL)
    text = text.lower().replace("\"", "").replace("'", "").replace(":", "").replace(".", "") \
        .replace("(", "").replace(")", "").replace(";", "") \
        .replace("?", "").replace("!", "").replace("#", "").replace("`", "") \
        .replace("[", "").replace("]", "") \
        .replace('\n', ' ').replace('\r', ' ')

    text = removeNonAscii(text)

    clean_text = ""

    for word in text.split():
        if word not in stopwords.words('english'):

            word = word.strip()

            if word.startswith("@"):
                word = "*ACCOUNT*"
            elif word.startswith("http"):
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


def getTweetsForKeyword(keyword, last_id=None):
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
        tso.setCount(100)
        tso.setIncludeEntities(True)

        if last_id is not None:
            tso.setSinceID(last_id)

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


def sentimentTweet(tweet):
    pos_score, neg_score = senti_classifier.polarity_scores([tweet])
    if pos_score > neg_score:
        vote = 1
    elif pos_score < neg_score:
        vote = -1
    else:
        vote = 0
    return vote


def extractLocation(tweet):
    try:
        location = tweet["place"]["country_code"]
    except Exception:
        location = ""
    return location


if __name__ == '__main__':

    counter = {}
    db = DBConnector()
    db.testDB()

    namer = Namer()

    company = keywords[0]

    random.shuffle(keywords, random.random)

    for keyword in keywords:

        last_id = db.getLastIdForQuery(keyword)
        print "last_id=", last_id
        tweet_list = getTweetsForKeyword(keyword, last_id)

        for tweet in tweet_list:

            creation_date = parser.parse(tweet["created_at"])
            country = extractLocation(tweet)
            tweet_id = int(tweet["id"])
            clean_text = normalize_tweet(tweet["text"]).encode("utf-8")

            try:
                account_date = parser.parse(tweet["user"]["created_at"])
            except:
                account_date = ""

            try:
                followers_count = int(tweet["user"]["followers_count"])
            except:
                followers_count = -1

            try:
                user_name = removeNonAscii(tweet["user"]["name"].split()[0])
                gender = namer.nameLookup(user_name)

            except:
                user_name = ""
                gender = ""

            if country != "":
                vote = sentimentTweet(clean_text)
                db.insertTweet(keyword, tweet_id, clean_text, country, creation_date, user_name, gender,
                               account_date, followers_count, vote)
                try:
                    counter[country] += vote
                except KeyError:
                    counter[country] = vote

            else:
                db.insertTweet(keyword, tweet_id, clean_text, country, creation_date, user_name, gender,
                               account_date, followers_count)




    write_it("M", 0, 0, keywords)
    write_it("M", 0, 1, keywords)
    write_it("M", 0, 2, keywords)
    write_it("M", 0, 3, keywords)
    write_it("M", 0, 4, keywords)

    write_it("M", 1, 0, keywords)
    write_it("M", 1, 1, keywords)
    write_it("M", 1, 2, keywords)
    write_it("M", 1, 3, keywords)
    write_it("M", 1, 4, keywords)

    write_it("M", 2, 0, keywords)
    write_it("M", 2, 1, keywords)
    write_it("M", 2, 2, keywords)
    write_it("M", 2, 3, keywords)
    write_it("M", 2, 4, keywords)

    write_it("M", 3, 0, keywords)
    write_it("M", 3, 1, keywords)
    write_it("M", 3, 2, keywords)
    write_it("M", 3, 3, keywords)
    write_it("M", 3, 4, keywords)

    write_it("M", 4, 0, keywords)
    write_it("M", 4, 1, keywords)
    write_it("M", 4, 2, keywords)
    write_it("M", 4, 3, keywords)
    write_it("M", 4, 4, keywords)

    
    write_it("F", 0, 0, keywords)
    write_it("F", 0, 1, keywords)
    write_it("F", 0, 2, keywords)
    write_it("F", 0, 3, keywords)
    write_it("F", 0, 4, keywords)

    write_it("F", 1, 0, keywords)
    write_it("F", 1, 1, keywords)
    write_it("F", 1, 2, keywords)
    write_it("F", 1, 3, keywords)
    write_it("F", 1, 4, keywords)

    write_it("F", 2, 0, keywords)
    write_it("F", 2, 1, keywords)
    write_it("F", 2, 2, keywords)
    write_it("F", 2, 3, keywords)
    write_it("F", 2, 4, keywords)

    write_it("F", 3, 0, keywords)
    write_it("F", 3, 1, keywords)
    write_it("F", 3, 2, keywords)
    write_it("F", 3, 3, keywords)
    write_it("F", 3, 4, keywords)

    write_it("F", 4, 0, keywords)
    write_it("F", 4, 1, keywords)
    write_it("F", 4, 2, keywords)
    write_it("F", 4, 3, keywords)
    write_it("F", 4, 4, keywords)


    write_it("A", 0, 0, keywords)
    write_it("A", 0, 1, keywords)
    write_it("A", 0, 2, keywords)
    write_it("A", 0, 3, keywords)
    write_it("A", 0, 4, keywords)

    write_it("A", 1, 0, keywords)
    write_it("A", 1, 1, keywords)
    write_it("A", 1, 2, keywords)
    write_it("A", 1, 3, keywords)
    write_it("A", 1, 4, keywords)

    write_it("A", 2, 0, keywords)
    write_it("A", 2, 1, keywords)
    write_it("A", 2, 2, keywords)
    write_it("A", 2, 3, keywords)
    write_it("A", 2, 4, keywords)

    write_it("A", 3, 0, keywords)
    write_it("A", 3, 1, keywords)
    write_it("A", 3, 2, keywords)
    write_it("A", 3, 3, keywords)
    write_it("A", 3, 4, keywords)

    write_it("A", 4, 0, keywords)
    write_it("A", 4, 1, keywords)
    write_it("A", 4, 2, keywords)
    write_it("A", 4, 3, keywords)
    write_it("A", 4, 4, keywords)