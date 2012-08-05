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

csvin = './CSVKraje/Kraje_TownPrecinctData.csv'

f = open(csvin, 'rb')
vesnicedata = csv.reader(f)

krajokres0 = []
for vesnice in vesnicedata:
    krajokresline = [int(vesnice[3]), int(vesnice[4])]
    krajokres0.append(krajokresline)

krajokres = []
for value in krajokres0:
    if value not in krajokres:
        krajokres.append(value) 

csvout = './CSVKraje/Kraje_CandDistrict.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['Kraj', 'Okres', 'KrajNazev', 'OkresNazev', 'Poradi', 'Jmeno', 'Vek', 'Hlasy', 'Procenta', 'Kandidatka', 'URL']
writer.writerow(headerrow)

pocetkandidatek = 60
vsechnykandidatky = range(1, pocetkandidatek + 1)

for okres in krajokres:
    for kandidatka in vsechnykandidatky:
        urldat = 'http://volby.cz/pls/kz2008/kz351?xjazyk=CZ&xdatum=20081017&xkraj=' + str(okres[0]) + '&xnumnuts=' + str(okres[1]) + '&xstrana=' + str(kandidatka)
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
        
        geoid = soup.find_all("h3")
        if len(geoid) != 0:
            krajname = geoid[0].contents[0].replace('Kraj: ','').strip()
            if okres[1] != 1100:
                okresname = geoid[1].contents[0].replace('Okres:', '').strip()
            else:
                okresname = "Praha"
        
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
                row = [okres[0], okres[1], krajname, okresname, poradiA, jmenoA, vekA, hlasyA, procentaA, kandidatka, urldat]
                if hlasyA != '-':
                    writer.writerow(row)