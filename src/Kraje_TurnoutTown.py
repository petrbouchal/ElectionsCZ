'''
Created on Mar 4, 2012

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

electyear = str(2012)
electdatestring = str(20121012)
electtype = 'Kraj'

poctyokrskusoubor = './CSVKraje/Kraje_TownPrecinctData_' + electtype + '_' + electyear + '.csv'

csvout = './CSVKraje/' + electtype + '_TurnoutTown_' + electyear + '.csv'

ucast = open(csvout, 'wb')
writer = csv.writer(ucast)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Okrsky', 'Volici', 'Vydane', \
             'Ucast', 'Odevzdane', 'Platne', 'PlatneProc', 'URL']
writer.writerow(headerrow)

f = open(poctyokrskusoubor, 'rb')
obcedata = csv.reader(f)
for vesnice in obcedata:
    urldat = 'http://volby.cz/pls/kz' + electyear + '/kz311?xjazyk=CZ&xdatum=' + electdatestring + '&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
    try:
        response = urllib2.urlopen(urldat)
    except IOError as (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
        print 'URL opening failed, trying again after 5 secs...'
        time.sleep(5)
        try:
            response = urllib2.urlopen(urldat)
        except IOError:
            print 'Tried again, didnt work'
            raise
    print urldat
    html0 = response.read()
    html = html0.replace('content="text/html;', 'content="text/html"')
    soup = BeautifulSoup(html, "lxml")
    # prettysoup = soup.prettify()
    okrsky = soup.find_all("td", { "headers" : "sa1 sb1" })
    volici = soup.find_all("td", { "headers" : "sa2" })
    vydane = soup.find_all("td", { "headers" : "sa3" })
    ucast = soup.find_all("td", { "headers" : "sa4" })
    odevzdane = soup.find_all("td", { "headers" : "sa5" })
    platne = soup.find_all("td", { "headers" : "sa6" })
    platneProc = soup.find_all("td", { "headers" : "sa7" })
    if len(odevzdane) != 0:
        okrskyB = okrsky[0].contents
        voliciB = volici[0].contents
        vydaneB = vydane[0].contents
        ucastB = ucast[0].contents
        odevzdaneB = odevzdane[0].contents
        platneB = platne[0].contents
        platneProcB = platneProc[0].contents
        print "\nObec: " + str(vesnice[1])
        okrskyA = okrskyB[0].replace(u' ', u'').replace(u'\xa0', u'')
        voliciA = voliciB[0].replace(u' ', u'').replace(u'\xa0', u'')
        vydaneA = vydaneB[0].replace(u' ', u'').replace(u'\xa0', u'')
        ucastA = ucastB[0].replace(u' ', u'').replace(u'\xa0', u'').replace(',', '.')
        odevzdaneA = odevzdaneB[0].replace(u' ', u'').replace(u'\xa0', u'')
        platneA = platneB[0].replace(u' ', u'').replace(u'\xa0', u'')
        platneProcA = platneProcB[0].replace(u' ', u'').replace(u'\xa0', u'').replace(',', '.')
        row = [vesnice[0], vesnice[1].encode('utf-8', 'replace'), vesnice[3], vesnice[4], okrskyA, voliciA, vydaneA, ucastA, odevzdaneA, platneA, platneProcA, urldat]
        writer.writerow(row)
