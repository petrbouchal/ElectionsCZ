'''
Created on Mar 21, 2012

@author: petrbouchal
'''
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

csvout = './CSVKraje/Kraje_CandPrecinct2.csv'
kandidati = open(csvout, 'wb')
writer = csv.writer(kandidati)
headerrow = ['Kraj', 'CisloObce', 'PoradiKand', 'KandJmeno', 'KandVek', 'Hlasy', 'Procenta', 'Okres', 'Kandidatka', 'Okrsek', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
okrskydata = csv.reader(f)
pocetkandidatek = 60
vsechnykandidatky = range(1, pocetkandidatek + 1)
for vesnice in okrskydata:
    # first, set the range to default, as in the case with one precinct
    vsechnyokrsky = range(1, int(vesnice[2]) + 1)
    # only do the following for multi-precinct towns
    if vesnice[2] > 1:
        urlvesnice = 'http://volby.cz/pls/kz2008/kz33?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0]
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
        html00 = vesnicehtml.read()
        html0 = html00.replace('content="text/html;','content="text/html"')
        soup0 = BeautifulSoup(html0, "lxml")
        cisloOkrsku = soup0.find_all("td", { "headers" : "t1s1" })
        prvnicislo0 = re.compile('>{1}[0-9]{1,4}<{1}')
        prvnicislo = prvnicislo0.findall(str(cisloOkrsku[0]))
        cislo0 = prvnicislo[0].replace('<','').replace('>','')
        cislo = int(cislo0)    
        if cislo == 1:
            vsechnyokrsky = range(1, int(vesnice[2]) + 1)
        else:
            vsechnyokrsky = range(cislo, cislo + int(vesnice[2]) + 1)
    for kandidatka in vsechnykandidatky:
        for okrsek in vsechnyokrsky:
            urldat = 'http://volby.cz/pls/kz2008/kz351?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0] + '&xokrsek=' + str(okrsek) + '&xstrana=' + str(kandidatka)
            print urldat
            try:
                response = urllib2.urlopen(urldat)
                obcedata = csv.reader(f)
            except IOError:
                print 'URL opening failed, trying again after 5 secs...'
                time.sleep(5)
                try:
                    response = urllib2.urlopen(urldat)
                    obcedata = csv.reader(f)
                except IOError:
                    print 'Tried again, didnt work'
                    raise                
            html0 = response.read()
            html = html0.replace('content="text/html;','content="text/html"')
            soup = BeautifulSoup(html, "lxml")
            # prettysoup = soup.prettify()
            poradi = soup.find_all("td", { "headers" : "t1sa1 t1sb1" })
            jmeno = soup.find_all("td", { "headers" : "t1sa1 t1sb2" })
            vek = soup.find_all("td", { "headers" : "t1sa1 t1sb3" })
            hlasy = soup.find_all("td", { "headers" : "t1sa2 t1sb4" })
            procenta = soup.find_all("td", { "headers" : "t1sa2 t1sb5" })
            poradi2 = soup.find_all("td", { "headers" : "t2sa1 t2sb1" })
            jmeno2 = soup.find_all("td", { "headers" : "t2sa1 t2sb2" })
            vek2 = soup.find_all("td", { "headers" : "t2sa1 t2sb3" })
            hlasy2 = soup.find_all("td", { "headers" : "t2sa2 t2sb4" })
            procenta2 = soup.find_all("td", { "headers" : "t2sa2 t2sb5" })                
            
            poradi.extend(poradi2) 
            jmeno.extend(jmeno2)
            vek.extend(vek2)
            hlasy.extend(hlasy2)
            procenta.extend(procenta2)               
            
            if len(poradi) != 0:
                for clovek in range(len(poradi)):
                    poradiB = poradi[clovek].contents
                    jmenoB = jmeno[clovek].contents
                    vekB = vek[clovek].contents
                    hlasyB = hlasy[clovek].contents
                    procentaB = procenta[clovek].contents                        
                    poradiA = poradiB[0].strip()
                    jmenoA = jmenoB[0].strip().encode('utf-8','replace')
                    print jmenoA
                    print '\n kandidatka: ' + str(kandidatka)
                    print "\n Okrsek: " + str(okrsek)
                    vekA = vekB[0].strip()
                    hlasyA = hlasyB[0].replace(u' ',u'').replace(u'\xa0',u'')
                    procentaA = procentaB[0].strip().replace(',','.')
                    if procentaA != '-':
                        row = [vesnice[3], vesnice[0], poradiA, jmenoA, vekA, hlasyA, procentaA, vesnice[4], kandidatka, okrsek, urldat]
                        writer.writerow(row)