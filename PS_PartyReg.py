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

csvout = './CSVPS/PS_PartyReg.csv'
strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['Kraj', 'Hlasy', 'Procenta', 'KandidatkaNazev', 'KandidatkaCislo', 'URL']
writer.writerow(headerrow)

kraje = range (1, 15)

for kraj in kraje:
    urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=' + str(kraj)
    print str(kraj) + ': ' + urldat
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
            cisloKandA = cisloKandB[0].strip().replace('&nbsp;','')
            nazevKandA = nazevKandB[0].strip().replace('&nbsp;','').encode('utf-8','replace')
            procentaA = procentaB[0].strip().replace('&nbsp;','').replace(',','.')
            row = [kraj, hlasyA,  procentaA, nazevKandA, cisloKandA, urldat]
            if hlasyA != '-':
                writer.writerow(row)