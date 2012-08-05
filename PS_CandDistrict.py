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
import re
# Import module to open webpages
import urllib2
# Import module to write csv files
import csv
import time

csvin = './CSVPS/PS_TownPrecinctData.csv'

csvout = './CSVPS/PS_CandDistrict.csv'

kandidati = open(csvout, 'wb')
writer = csv.writer(kandidati)
headerrow = ['Kraj', 'Okres', 'KrajNazev', 'OkresNazev' 'Poradi', 'Jmeno', 'Vek', 'Hlasy', 'Procenta', 'Kandidatka', 'URL']
writer.writerow(headerrow)

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

vsechnykandidatky = range(1, 27)
for okres in krajokres:
    print okres[1]
    for partaj in vsechnykandidatky:
        urldat = 'http://volby.cz/pls/ps2010/ps351?xjazyk=CZ&xkraj=' + str(okres[0]) + '&xnumnuts=' + str(okres[1]) + '&xstrana=' + str(partaj)
        print 'Strana:' + str(partaj) + ' ' + urldat
        try:
            response = urllib2.urlopen(urldat)
            obcedata = csv.reader(f)
        except IOError as (errno, strerror):
            print "I/O error({0}): {1}".format(errno, strerror)
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
        
        geoid = soup.find_all("h3")
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
                vekA = vekB[0].strip()
                hlasyA = hlasyB[0].replace(u' ',u'').replace(u'\xa0',u'')
                procentaA = procentaB[0].replace(',','.').replace(u' ',u'').replace(u'\xa0',u'')
                row = [okres[0], okres[1], krajname, okresname, poradiA, jmenoA, vekA, hlasyA, procentaA, partaj, urldat]
                if poradiA != '-':
                    writer.writerow(row)
                    print jmenoA
            