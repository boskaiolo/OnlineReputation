__author__ = "Alberto Boschetti"
__status__ = "Prototype"


import sqlite3


class DBConnector:

    #DEFINE
    DBname = "../db/db.sqlite3"

    def testDB(self):
        """
        Check the file. If not, it creates it with the right structure
        """
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            print "SQLite version: %s" % cur.fetchone()

            cur.execute("CREATE TABLE IF NOT EXISTS idTweets("
                        "query TEXT NOT NULL, "
                        "twitter_id INTEGER NOT NULL PRIMARY KEY, "
                        "clean_text TEXT NOT NULL, "
                        "country TEXT DEFAULT \"\", "
                        "sentiment INT DEFAULT 0, "
                        "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                        "user_name TEXT DEFAULT \"\", "
                        "gender TEXT DEFAULT \"\","
                        "registration_date TIMESTAMP,"
                        "followers INT DEFAULT 0)")
            print "TABLE idTweets OK"

    def cleanAllValues(self):
        con = sqlite3.connect(self.DBname)

        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM idTweets')

    def insertTweet(self, queryterms, twitterid, clean_text, country, creation_date, user_name, gender,
                    registration_date, followers, sentiment=0):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            try:
                query = 'INSERT INTO idTweets' \
                        '(query, twitter_id, clean_text, country, sentiment, timestamp, user_name, gender,' \
                        ' registration_date, followers) \
                         VALUES ' \
                        '("{val1}", {val2}, "{val3}", "{val4}", {val5}, "{val6}", "{val7}", "{val8}", "{val9}", {val10})' \
                    .format(val1=queryterms, val2=twitterid, val3=clean_text.encode("utf-8"), val4=country, val5=sentiment,
                            val6=creation_date, val7=user_name.decode("utf-8"), val8=gender, val9=registration_date,
                            val10=followers)
                cur.execute(query)
            except sqlite3.IntegrityError:
                pass # trying to re-insert the same tweet!
            except Exception as e:
                print "[ERROR] ", queryterms, twitterid, clean_text, country, creation_date, user_name, gender, sentiment
                print e, e.message

    def getSentimentWithFilter(self, gender, twitter_usage, popularity, queryterm_list):
        con = sqlite3.connect(self.DBname)

        or_clause = "WHERE (1=0"
        for word in queryterm_list:
            or_clause += " OR query=\"" + word + "\""
        or_clause += ")"

        if gender=="M" or gender == "F":
            or_clause += " AND gender = \"" + gender + "\" "

        if twitter_usage==1:
            or_clause += ' AND registration_date > date("now", "-1 month") '
        elif twitter_usage==2:
            or_clause += ' AND registration_date BETWEEN date("now", "-1 year") AND date("now", "-1 month") '
        elif twitter_usage==3:
            or_clause += ' AND registration_date BETWEEN date("now", "-2 year") AND date("now", "-1 year") '
        elif twitter_usage==4:
            or_clause += ' AND registration_date < date("now", "-2 year") '

        if popularity==1:
            or_clause += ' AND followers <= 10 '
        elif popularity==2:
            or_clause += ' AND followers > 10 AND followers <= 100 '
        elif popularity==3:
            or_clause += ' AND followers > 100 AND followers <= 1000 '
        elif popularity==4:
            or_clause += ' AND followers > 1000 '

        with con:
            cur = con.cursor()
            query = 'SELECT country, sum(sentiment) as sentiment_score ' \
                    'FROM idTweets {clause} GROUP BY country' \
                .format(clause=or_clause)
            try:
                cur.execute(query)
                return cur.fetchall()
            except Exception as e:
                print "[ERROR]", query, e.message


    def getLastIdForQuery(self, queryterm):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            query = 'SELECT MAX(twitter_id) FROM idTweets WHERE query=\"{val1}\"' \
                .format(val1=queryterm)
            try:
                cur.execute(query)
                val = cur.fetchall()[0][0]
                return val
            except Exception as e:
                print "[ERROR]", query, e.message
