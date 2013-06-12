import glob
import os

__author__ = "Alberto Boschetti"
__status__ = "Prototype"


def array_to_html_page(arr, company):

    """
    Make the js vector for the html file. Write to <data/company.js>, and to data/data.js
    :param arr: the (country, sentiment_count) vector
    :param company: the company's name
    """
    arrstring = 'data["' + company + '"] = ['
    arrstring += "['Country', 'Sentiment'],"
    for entry in arr:
        arrstring += "[\'" + entry[0] + "\'," + str(entry[1]) + "],"
    arrstring = arrstring[:-1]
    arrstring += '];'


    fh = open("../data/" + company + ".js", "w")
    fh.write(arrstring)
    fh.close()

    # merge them in a unique file
    try:
        os.remove('../data/data.js')
    except:
        pass


    jsfiles = glob.glob('../data/*.js')
    f = open("../data/data.js", "w")
    for tempfile in jsfiles:
        fh = open(tempfile, "r")
        f.write(fh.readline())
        fh.close()
