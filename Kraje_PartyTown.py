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

csvin = './CSVKraje/Kraje_TownPrecinctData.csv'

csvout = './CSVKraje/Kraje_PartyTown.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Hlasy', 'Procenta', 'KandidatkaNazev', 'KandidatkaCislo', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
vesnicedata = csv.reader(f)
for vesnice in vesnicedata:
    urldat = 'http://volby.cz/pls/kz2008/kz311?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
    print vesnice[1] + ': ' + urldat
    try:
        response = urllib2.urlopen(urldat)
    except IOError as (errno, strerror):
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
        
    if len(cisloKand) != 0:
        for strana in range(len(cisloKand)):
            # print 'Strana cislo: ' + str(strana)
            cisloKandB = cisloKand[strana].contents
            nazevKandB = nazevKand[strana].contents
            hlasyB = hlasy[strana].contents
            procentaB = procenta[strana].contents                        
            hlasyA = hlasyB[0].replace(u' ',u'').replace(u'\xa0',u'')
            procentaA = procentaB[0].replace(u' ',u'').replace(u'\xa0',u'').replace(',','.')
            cisloKandA = cisloKandB[0].replace(u' ',u'').replace(u'\xa0',u'')
            nazevKandA = nazevKandB[0].replace(u' ',u'').replace(u'\xa0',u'').encode('utf-8','replace')
            row = [vesnice[0], vesnice[1].encode('utf-8','replace'), vesnice[3], vesnice[4], hlasyA,  procentaA, nazevKandA, cisloKandA, urldat]
            if hlasyA != '-':
                writer.writerow(row)