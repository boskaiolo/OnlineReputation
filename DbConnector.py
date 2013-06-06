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

            cur.execute("CREATE TABLE IF NOT EXISTS idTweets(twitter_id INTEGER NOT NULL PRIMARY KEY, clean_text TEXT, country TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
            print "TABLE idTweets OK"

    def cleanAllValues(self):
        con = sqlite3.connect(self.DBname)

        with con:
            cur = con.cursor()
            cur.execute('DELETE FROM idTweets')

    def insertTweet(self, id, clean_text, country):
        con = sqlite3.connect(self.DBname)
        with con:
            cur = con.cursor()
            query = 'INSERT INTO idTweets(twitter_id, clean_text, country) VALUES ({val1}, "{val2}", "{val3}")'.format(val1=id, val2=clean_text, val3=country)
            try:
                cur.execute(query)
            except sqlite3.IntegrityError:
                pass #re-insert the same tweet
            except Exception as e:
                print "[ERROR]", query, e.message


    def getTweets(self, timestampFrom=None, timestampTo=None):
        print "TODO"
