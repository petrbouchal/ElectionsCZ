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

csvin = './CSVPS/PS_TownPrecinctData.csv'

csvout = './CSVPS/PS_TurnoutTown.csv'
okrsky = open(csvout, 'wb')
writer = csv.writer(okrsky)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Okrsky', 'Volici', 'Vydane', 'Ucast', 'Odevzdane', 'Platne', 'PlatneProc', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
vesnicedata = csv.reader(f)
for vesnice in vesnicedata:
    urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
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
    volici = soup.find_all("td", { "headers" : "sa2" })
    okrsky = soup.find_all("td", { "headers" : "sa1 sb1" })
    vydane = soup.find_all("td", { "headers" : "sa3" })
    ucast = soup.find_all("td", { "headers" : "sa4" })
    odevzdane = soup.find_all("td", { "headers" : "sa5" })
    platne = soup.find_all("td", { "headers" : "sa6" })
    platneProc = soup.find_all("td", { "headers" : "sa7" })
    if len(odevzdane) != 0:
        voliciB = volici[0].contents
        okrskyB = okrsky[0].contents
        vydaneB = vydane[0].contents
        ucastB = ucast[0].contents
        odevzdaneB = odevzdane[0].contents                        
        platneB = platne[0].contents
        platneProcB = platneProc[0].contents
        voliciA = voliciB[0].replace(u' ',u'').replace(u'\xa0',u'') 
        okrskyA = okrskyB[0].replace(u' ',u'').replace(u'\xa0',u'') 
        vydaneA = vydaneB[0].replace(u' ',u'').replace(u'\xa0',u'') 
        ucastA = ucastB[0].replace(u' ',u'').replace(u'\xa0',u'').replace(',','.')
        odevzdaneA = odevzdaneB[0].replace(u' ',u'').replace(u'\xa0',u'')         
        platneA = platneB[0].replace(u' ',u'').replace(u'\xa0',u'')
        platneProcA = platneProcB[0].replace(u' ',u'').replace(u'\xa0',u'').replace(',','.')
        row = [vesnice[1], vesnice[0].encode('utf-8','replace'), vesnice[4], vesnice[3], okrskyA, voliciA, vydaneA, ucastA, odevzdaneA, platneA, platneProcA, urldat]
        writer.writerow(row)