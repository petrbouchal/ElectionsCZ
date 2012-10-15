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

csvout = './CSVPS/PS_PartyDistrict.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['Kraj', 'Okres', 'KrajNazev', 'OkresNazev', 'Hlasy', 'Procenta', 'KandidatkaNazev', 'KandidatkaCislo', 'URL']
writer.writerow(headerrow)

for okres in krajokres:
    urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=' + str(okres[0]) + '&xnumnuts=' + str(okres[1])
    # make an exception url for Prague:
    if okres[1] == 1100:
        urldat = 'http://volby.cz/pls/ps2010/ps311?xjazyk=CZ&xkraj=1'
    print 'Kraj ' + str(okres[0]) + ', okres ' + str(okres[1]) + ': \n' + urldat
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
    
    geoid = soup.find_all("h3")
    krajname = geoid[0].contents[0].replace('Kraj: ','').strip()
    if okres[1] != 1100:
        okresname = geoid[1].contents[0].replace('Okres:', '').strip()
    else:
        okresname = "Praha"
    
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
            cisloKandA = cisloKandB[0].replace(u' ',u'').replace(u'\xa0',u'')
            nazevKandA = nazevKandB[0].strip().encode('utf-8','replace')
            procentaA = procentaB[0].strip().replace(',','.')
            row = [okres[0], okres[1], krajname, okresname, hlasyA,  procentaA, nazevKandA, cisloKandA, urldat]
            if hlasyA != '-':
                writer.writerow(row)