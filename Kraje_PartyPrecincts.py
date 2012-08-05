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

csvin = './CSVKraje/Kraje_TownPrecinctData.csv'

csvout = './CSVKraje/Kraje_PartyPrecinct.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['Kraj', 'CisloObce', 'NazevObce', 'Hlasy', 'Procenta', 'KandidatkaNazev', 'KandidatkaCislo', 'Okres', 'Okrsek', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
okrskydata = csv.reader(f)
for vesnice in okrskydata:
    # first, set the range to default, as in the case with one precinct
    vsechnyokrsky = range(1, int(vesnice[2]) + 1)
    # only do the following for multi-precinct towns
    if vesnice[2] > 1:
        urlvesnice = 'http://volby.cz/pls/kz2008/kz33?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
        print urlvesnice
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
        html0 = response.read()
        html = html0.replace('content="text/html;','content="text/html"')
        soup0 = BeautifulSoup(html, "lxml")
        cisloOkrsku = soup0.find_all("td", { "headers" : "t1s1" }, limit=1)
        prvnicislo0 = re.compile('>{1}[0-9]{1,4}<{1}')
        prvnicislo = prvnicislo0.findall(str(cisloOkrsku[0]))
        cislo0 = prvnicislo[0].replace('<','').replace('>','')
        cislo = int(cislo0)    
        if cislo == 1:
            vsechnyokrsky = range(1, int(vesnice[2]) + 1)
        else:
            vsechnyokrsky = range(cislo, cislo + int(vesnice[2]) + 1)
    for okrsek in vsechnyokrsky:
        urldat = 'http://volby.cz/pls/kz2008/kz311?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0] + '&xokrsek=' + str(okrsek)
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
        html = response.read()
        soup = BeautifulSoup(html)
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
                cisloKandB = cisloKand[strana].contents
                nazevKandB = nazevKand[strana].contents
                hlasyB = hlasy[strana].contents
                procentaB = procenta[strana].contents                        
                hlasyA = hlasyB[0].replace(u' ',u'').replace(u'\xa0',u'')
                procentaA = procentaB[0].strip()
                print "Okrsek: " + str(okrsek)
                cisloKandA = cisloKandB[0].strip()
                nazevKandA = nazevKandB[0].strip().encode('utf-8','replace')
                procentaA = procentaB[0].strip().replace(',','.')
                if procentaA != "-":
                    row = [vesnice[3], vesnice[1].encode('utf-8','replace'), vesnice[0], hlasyA,  procentaA, nazevKandA, cisloKandA, vesnice[4], okrsek, urldat]
                    writer.writerow(row)