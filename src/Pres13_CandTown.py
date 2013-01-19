'''
Created on Jan 12, 2013

@author: petrbouchal
'''
# Import the BeautifulSoup HTML parser
from bs4 import BeautifulSoup
# Import the regular expression module
# import re
# Import module to open webpages
import urllib2
# Import module to write csv files
import csv
import time

electyear = str(2013)
electtype = 'PR'
votetype = 'Hlasy' # can be "Hlasy", "PrefHlasy" or "Ucast"
unitobs = 'StranaObec' # specify unit of observation and unit of aggregation
votinground = 'round1'

datatype = 'votes' # can be votes or live

csvin = '../data-input/' + electtype + '13' + '_ObceOkrsky.csv'

csvout = '../data-' + datatype + '/' + electtype + electyear + '_'\
 + votetype + '_' + unitobs + '_' + votinground + '.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Hlasy', \
             'Procenta', 'KandidatJmeno', 'KandidatCislo', \
             'Okrsky', 'Volici', 'ObalkyVydane', 'ObalkyVhozene', 'Ucast', 'PlatneHlasy', 'PlatneProc', \
             'URL']

writer.writerow(headerrow)

obcedata = csv.DictReader(open(csvin, "rb"))

baseurl = 'http://volby.cz/pls/prez2013/'

for obec in obcedata:
    urldat = 'http://volby.cz/pls/prez' + electyear + '/pe311?xjazyk=CZ&xnumnuts='\
    + obec['NumNUTS'] + '&xobec=' + obec['CisloObce']
    print obec['NazevObce'] + ': ' + urldat
    try:
        response = urllib2.urlopen(urldat)
    except IOError:
        print 'URL opening failed, trying again after 5 secs...'
        time.sleep(5)
        try:
            response = urllib2.urlopen(urldat)
        except IOError:
            print 'Tried again, didn\'t work'
            raise
    html0 = response.read()
    html = html0.replace('content="text/html;', 'content="text/html"')
    soup = BeautifulSoup(html, "lxml")

    cisloKand = soup.find_all("td", { "headers" : "t1sa1 t1sb1" })
    nazevKand = soup.find_all("td", { "headers" : "t1sa1 t1sb2" })
    hlasy = soup.find_all("td", { "headers" : "t1sa2 t1sb3" })
    procenta = soup.find_all("td", { "headers" : "t1sa2 t1sb4" })
    cisloKand2 = soup.find_all("td", { "headers" : "t2sa1 t2sb1" })
    nazevKand2 = soup.find_all("td", { "headers" : "t2sa1 t2sb2" })
    hlasy2 = soup.find_all("td", { "headers" : "t2sa2 t2sb3" })
    procenta2 = soup.find_all("td", { "headers" : "t2sa2 t2sb4" })

    cisloKand.extend(cisloKand2)
    nazevKand.extend(nazevKand2)
    hlasy.extend(hlasy2)
    procenta.extend(procenta2)

    okrskyAll = soup.find_all("td", { "headers" : "sa1 sb1" })[0].contents[0]
    okrskyCounted = soup.find_all("td", { "headers" : "sa1 sb2" })[0].contents[0]
    okrskyProc = soup.find_all("td", { "headers" : "sa1 sb3" })[0].contents[0].replace(",", ".")
    votersAll = soup.find_all("td", { "headers" : "sa2" })[0].contents[0].replace(' ', '').replace(u'\xa0', u'')
    votersCame = soup.find_all("td", { "headers" : "sa3" })[0].contents[0].replace(' ', '').replace(u'\xa0', u'')
    votersProc = soup.find_all("td", { "headers" : "sa4" })[0].contents[0].replace(",", ".")
    votersCast = soup.find_all("td", { "headers" : "sa5" })[0].contents[0].replace(' ', '').replace(u'\xa0', u'')
    votersValid = soup.find_all("td", { "headers" : "sa6" })[0].contents[0].replace(' ', '').replace(u'\xa0', u'')
    votersValidProc = soup.find_all("td", { "headers" : "sa7" })[0].contents[0].replace(",", ".")

    row = []

    writer.writerow(row)
