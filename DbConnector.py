__author__ = "Alberto Boschetti"
__status__ = "Prototype"


import sqlite3


class DBConnector:

    #DEFINE
    DBname = "db.sqlite3"

    def testDB(self):
        """
        Check the file. If not, it creates it with the right structure
        """
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            cur.execute('SELECT SQLITE_VERSION()')
            print "SQLite version: %s" % cur.fetchone()

            cur.execute("CREATE TABLE IF NOT EXISTS idTweets(query TEXT NOT NULL, twitter_id INTEGER NOT NULL PRIMARY KEY, clean_text TEXT NOT NULL, country TEXT DEFAULT \"unknown\", sentiment INT DEFAULT 0, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print "TABLE idTweets OK"

    def cleanAllValues(self):
        con = sqlite3.connect(self.DBname)

        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM idTweets')

    def insertTweet(self, queryterms, id, clean_text, country, sentiment=0):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            query = 'INSERT INTO idTweets(query, twitter_id, clean_text, country, sentiment) VALUES ("{val1}", {val2}, "{val3}", "{val4}", {val5})'\
                    .format(val1=queryterms, val2=id, val3=clean_text, val4=country, val5=sentiment)
            try:
                cur.execute(query)
            except sqlite3.IntegrityError:
                pass #re-insert the same tweet
            except Exception as e:
                print "[ERROR]", query, e.message

    def getSentimentTweets(self, queryterms, timestampFrom=None, timestampTo=None):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            query = 'SELECT country, sum(sentiment) as sentiment_score FROM idTweets WHERE query=\"{val1}\" GROUP BY country' \
                .format(val1=queryterms)
            try:
                cur.execute(query)
                return cur.fetchall()
            except Exception as e:
                print "[ERROR]", query, e.message

    def cleanEntryForQuery(self, queryterms):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            query = 'DELETE FROM idTweets WHERE query=\"{val}\"'\
                    .format(val=queryterms)
            cur.execute(query)
