'''
Created on Jan 11, 2013

@author: petrbouchal
'''

from bs4 import BeautifulSoup
# import re
import urllib2
import csv
import time
from datetime import datetime
import sys

print sys.getdefaultencoding()

# set parameters
url = 'http://volby.cz/pls/prez2013/pe2?xjazyk=CZ'

electyear = str(2013)
electdatestring = str(20121012)
electtype = 'PR'
votetype = 'Hlasy' # can be "Hlasy", "PrefHlasy" or "Ucast"
unitobs = 'StranaObec' # specify unit of observation and unit of aggregation
votinground = 'round1'
datatype = 'votes' # can be votes or live

csvout = './data-' + datatype + '/' + electtype + electyear + '_'\
 + votetype + '_' + unitobs + '_' + votinground + '.csv'

kandidati = open(csvout, 'ab', 0)
writer = csv.writer(kandidati)
headerrow = ['KandCislo', 'KandJmeno', 'Hlasy', 'Procenta', 'Okrsky',
             'OkrskyZprac', 'Volici', 'Vydane', 'Odevzdane', 'Platne', 'Cas']
writer.writerow(headerrow)

while(1 == 1):
    cas = datetime.strftime(datetime.now(), '%Y-%d-%m-T%H:%M:%S')
    try:
        response = urllib2.urlopen(url)
    except IOError:
        print("Opening url" + url + "failed, trying again.")
        try:
            response = urllib2.urlopen(url)
        except IOError:
            print("Second try failed, aborting")
            continue
    html0 = response.read()
    html = html0.replace('content="text/html;', 'content="text/html"')
    soup = BeautifulSoup(html, "lxml")

    candnum = soup.find_all("td", { "headers" : "s2a1 s2b1" })
    candname = soup.find_all("td", { "headers" : "s2a1 s2b2" })
    votes = soup.find_all("td", { "headers" : "s2a5 s2b3" })
    percent = soup.find_all("td", { "headers" : "s2a6 s2b5" })

    okrsky = soup.find_all("td", { "headers" : "s1a1 s1b1" })[0].contents[0].replace(u'\xa0', u'')
    zpracovane = soup.find_all("td", { "headers" : "s1a1 s1b2" })[0].contents[0].replace(u'\xa0', u'')
    volici = soup.find_all("td", { "headers" : "s1a2" })[0].contents[0].replace(u'\xa0', u'')
    vydane = soup.find_all("td", { "headers" : "s1a3" })[0].contents[0].replace(u'\xa0', u'')
    odevzdane = soup.find_all("td", { "headers" : "s1a5" })[0].contents[0].replace(u'\xa0', u'')
    platne = soup.find_all("td", { "headers" : "s1a6" })[0].contents[0].replace(u'\xa0', u'')

    for clovek in range(len(candnum)):
        KandCislo = candnum[clovek].contents[0].strip().encode('utf-8', 'replace')
        KandJmeno = candname[clovek].contents[0].strip().encode('utf-8', 'replace')
        KandHlasy = votes[clovek].contents[0].strip().encode('utf-8', 'replace').replace(u'\xa0', u'')
        KandProcenta = percent[clovek].contents[0].strip().encode('utf-8', 'replace').replace(',', '.')
        row = [KandCislo, KandJmeno, KandHlasy, KandProcenta,
              okrsky, zpracovane, volici, vydane, odevzdane, platne, cas]
        print row
        writer.writerow(row)

        #file.close(kandidati)

    for i in range(0, 30):
        print "waiting 10 seconds",
        for i in range(0, 9):
            time.sleep(1)
            print("."),
        time.sleep(1)
        print (".")
    print "5 minutes elapsed, downloading"


