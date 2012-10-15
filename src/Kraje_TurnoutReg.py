'''
Created on Mar 22, 2012

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
import re

csvout = './CSVKraje/Kraje_TurnoutReg.csv'
okrsky = open(csvout, 'wb')
writer = csv.writer(okrsky)
headerrow = ['Kraj', 'Zastupitele', 'Okrsky', 'Volici', 'Vydane', 'Ucast', 'Odevzdane', 'Platne', 'PlatneProc', 'URL']
writer.writerow(headerrow)

kraje = range (1, 15)

for kraj in kraje:
    urldat = 'http://volby.cz/pls/kz2008/kz311?xjazyk=CZ&xdatum=20081017&xkraj=' + str(kraj)
    print urldat
    try:
        response = urllib2.urlopen(urldat)
    except IOError:
        print 'URL opening failed, trying again after 5 secs...'
        time.sleep(5)
        try:
            response = urllib2.urlopen(urldat)
        except IOError:
            print 'Tried again, didnt work'
            raise
    html0 = response.read()
    html = html0.replace('content="text/html;','content="text/html"')
    soup = BeautifulSoup(html, "lxml")
    # prettysoup = soup.prettify()
    zastupitele = soup.find_all("td", { "headers" : "sua0" })
    okrsky = soup.find_all("td", { "headers" : "sua1 sub1" })
    volici = soup.find_all("td", { "headers" : "sua2" })
    vydane = soup.find_all("td", { "headers" : "sua3" })
    ucast = soup.find_all("td", { "headers" : "sua4" })
    odevzdane = soup.find_all("td", { "headers" : "sua5" })
    platne = soup.find_all("td", { "headers" : "sua6" })
    platneProc = soup.find_all("td", { "headers" : "sua7" })
    if len(odevzdane) != 0:
        voliciB = volici[0].contents
        vydaneB = okrsky[0].contents
        zastupiteleB = zastupitele[0].contents
        okrskyB = okrsky[0].contents
        ucastB = ucast[0].contents
        odevzdaneB = odevzdane[0].contents                        
        platneB = platne[0].contents
        platneProcB = platneProc[0].contents
        print "Kraj: " + str(kraj)
        voliciA = voliciB[0].replace(u' ',u'').replace(u'\xa0',u'')
        vydaneA = vydaneB[0].replace(u' ',u'').replace(u'\xa0',u'')
        zastupiteleA = zastupiteleB[0].replace(u' ',u'').replace(u'\xa0',u'')
        okrskyA = okrskyB[0].replace(u' ',u'').replace(u'\xa0',u'')
        ucastA = ucastB[0].replace(',','.').replace(u' ',u'').replace(u'\xa0',u'')
        odevzdaneA = odevzdaneB[0].replace(u' ',u'').replace(u'\xa0',u'')         
        platneA = platneB[0].replace(u' ',u'').replace(u'\xa0',u'')
        platneProcA = platneProcB[0].replace(',','.').replace(u' ',u'').replace(u'\xa0',u'')
        row = [kraj, zastupiteleA, okrskyA, voliciA, vydaneA, ucastA, odevzdaneA, platneA, platneProcA, urldat]
        writer.writerow(row)