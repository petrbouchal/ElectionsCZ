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
import re

csvin = './CSVPS/PS_TownPrecinctData.csv'

csvout = './CSVPS/PS_TurnoutPrecinct.csv'
strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Okrsky', 'Volicu', 'Ucast', 'UcastProc', 'Odevzdane', 'Platne', 'PlatneProc', 'Okrsek', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
okrskydata = csv.reader(f)
for vesnice in okrskydata:
    # first, set the range to default, as in the case with one precinct
    vsechnyokrsky = range(1, int(vesnice[2]) + 1)
    # only do the following for multi-precinct towns
    if vesnice[2] > 1:
        urlvesnice = 'http://volby.cz/pls/ps2010/ps33?xjazyk=CZ&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
        try:
            vesnicehtml = urllib2.urlopen(urlvesnice)
        except IOError:
            print 'URL opening failed, trying again after 5 secs...'
            time.sleep(5)
            try:
                response = urllib2.urlopen(urlvesnice)
            except IOError:
                print 'Tried again, didnt work'
                raise
        html0 = vesnicehtml.read()
        soup0 = BeautifulSoup(html0, "html.parser")
        cisloOkrsku = soup0.find_all("td", { "headers" : "s1" }, limit=1)
        prvnicislo0 = re.compile('>{1}[0-9]{1,4}<{1}')
        prvnicislo = prvnicislo0.findall(str(cisloOkrsku[0]))
        cislo0 = prvnicislo[0].replace('<','').replace('>','')
        cislo = int(cislo0)    
        if cislo == 1:
            vsechnyokrsky = range(1, int(vesnice[2]) + 1)
        else:
            vsechnyokrsky = range(cislo, cislo + int(vesnice[2]) + 1)
    for okrsek in vsechnyokrsky:
        okrseknum = okrsek
        if vesnice[2] == 1:        
            urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0] + '&xvyber=' + vesnice[4]
        else:
            urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0] + '&xokrsek=' + str(okrseknum) + '&xvyber=' + vesnice[4]
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
            row = [vesnice[0], vesnice[1].encode('utf-8','replace'), vesnice[4], vesnice[3], okrskyA, voliciA, vydaneA, ucastA, odevzdaneA, platneA, platneProcA, urldat]
            writer.writerow(row)