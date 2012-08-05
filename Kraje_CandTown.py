'''
Created on Mar 22, 2012

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

csvin = './CSVKraje/Kraje_TownPrecinctData.csv'

csvout = './CSVKraje/Kraje_CandTown.csv'
kandidati = open(csvout, 'wb')
writer = csv.writer(kandidati)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Poradi', 'Jmeno', 'Vek', 'Hlasy', 'Procenta', 'Kandidatka', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
okrskydata = csv.reader(f)
pocetkandidatek = 60
vsechnykandidatky = range(1, pocetkandidatek + 1)
for vesnice in okrskydata:
    print vesnice[1]
    for kandidatka in vsechnykandidatky:
        urldat = 'http://volby.cz/pls/kz2008/kz351?xjazyk=CZ&xdatum=20081017&xkraj=' + vesnice[3] + '&xobec=' + vesnice[0] + '&xstrana=' + str(kandidatka)
        print 'Strana:' + str(kandidatka) + ' ' + urldat
        try:
            response = urllib2.urlopen(urldat)
            obcedata = csv.reader(f)
        except IOError:
            print 'URL opening failed, trying again after 5 secs...'
            time.sleep(5)
            try:
                print 'Trying again...'
                response = urllib2.urlopen(urldat)
                obcedata = csv.reader(f)
            except IOError:
                print 'Tried again, didnt work.'
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
                vekA = vekB[0].strip()
                hlasyA = hlasyB[0].replace(u' ',u'').replace(u'\xa0',u'')
                procentaA = procentaB[0].strip().replace(',','.')
                row = [vesnice[0], vesnice[1].encode('utf-8','replace'), vesnice[4], vesnice[3], poradiA, jmenoA, vekA, hlasyA, procentaA, kandidatka, urldat]
                if hlasyA != '-':
                    writer.writerow(row)