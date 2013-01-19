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
from datetime import datetime

electyear = str(2012)
electdatestring = str(20121012)
electtype = 'KZ'
votetype = 'Hlasy' # can be "Hlasy", "PrefHlasy" or "Ucast"
unitobs = 'KandidatObec' # specify unit of observation and unit of aggregation

csvin = './data-input/' + electtype + electyear + '_ObceOkrsky.csv'

csvout = './data-votes/' + electtype + electyear + '/' + electtype + \
         electyear + votetype + "_" + unitobs + '.csv'
kandidati = open(csvout, 'wb')
writer = csv.writer(kandidati)
headerrow = ['CisloObce', 'NazevObce', 'Okres', 'Kraj', 'Poradi', 'Jmeno', \
             'JmenoPrijmeni', 'Titul', \
             'Vek', 'Hlasy', 'Procenta', 'Kandidatka', 'URL']
writer.writerow(headerrow)

f = open(csvin, 'rb')
okrskydata = csv.reader(f)

## find out which parties ran in which regions
# fetch page with links to all party-region results
xurl = 'http://volby.cz/pls/kz' + electyear + '/kz11?xjazyk=CZ&xdatum=' + electdatestring + '&xv=1&xt=1'
x = urllib2.urlopen(xurl).read()
x0 = x.replace('content="text/html;', 'content="text/html"')
x1 = BeautifulSoup(x0)
regpartylinks = x1.find_all("a")

#build a list of these links
regpartyodkazy = []
for link in regpartylinks:
    odkaz0 = link['href'].strip()
    odkaz = 'http://volby.cz/pls/kz2012/' + odkaz0
    regpartyodkazy.append(odkaz)

print "Found approx. " + str(len(regpartyodkazy)) + " links to party-region results pages."

# prepare for list of links to all party-town results and equivalent party-region pages
f = open(csvin, 'rb')
obcedata = csv.reader(f)

pocetkandidatek = 95
vsechnykandidatky = range(1, pocetkandidatek + 1)

# build list of party-town links, leaving in only those where the equivalent party-region link exists
urldatlist = []
vesnicecount = 0
matchcount = 0
print "Matching generated link list with real candidate-region links. May take a while..."
for vesnice in okrskydata:
    for strana in vsechnykandidatky:
        urldat = 'http://volby.cz/pls/kz' + electyear + '/kz351?xjazyk=CZ&xdatum=' + electdatestring + '&xkraj='\
        + vesnice[3] + '&xstrana=' + str(strana) + '&xobec=' + vesnice[0]
        urlkraj = 'http://volby.cz/pls/kz' + electyear + '/kz111?xjazyk=CZ&xdatum=' + electdatestring + '&xkraj='\
        + vesnice[3] + '&xstrana=' + str(strana) + '&xv=1&xt=1'

        if urlkraj in regpartyodkazy:
            urldatlist.append(urldat)
        matchcount += 1
    vesnicecount += 1

print "Seznam linku na obce ma " + str(len(urldatlist)) + " linku."
print 'Looked across ' + str(vesnicecount) + ' towns.' + ' Tried ' + str(matchcount) + ' links.'

roundcounter = 0
startTime = datetime.now()
for urldat in urldatlist:
    print urldat
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
            print 'Tried again, didn\'t work.'
            raise
    html0 = response.read()
    html = html0.replace('content="text/html;', 'content="text/html"')
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

    # recover party list number
    chunk1 = re.findall(r'[&xstrana=][0-9]{1,2}&', urldat)
    chunk2 = re.findall(r'[0-9]{1,2}', chunk1[0])
    kandidatka = chunk2[0]

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
            jmenoA = jmenoB[0].strip().encode('utf-8', 'replace')

            vekA = vekB[0].strip()
            hlasyA = hlasyB[0].replace(u' ', u'').replace(u'\xa0', u'')
            procentaA = procentaB[0].strip().replace(',', '.')
            row = [vesnice[0], vesnice[1].encode('utf-8', 'replace'), \
                   vesnice[4], vesnice[3], poradiA, jmenoA,
                   vekA, hlasyA, \
                   procentaA, kandidatka, urldat]
            if hlasyA != '-':
                writer.writerow(row)
    roundcounter += 1
    if roundcounter % 100 == 0:
        secondselapsed = (datetime.now() - startTime).seconds
        sharedone = float(roundcounter) / float(len(urldatlist))
        print "Progress: " + str(round(sharedone * 100, 2)) + "%"
        print 'It took: ' + str(secondselapsed) + ' seconds'
        print 'ETA in: ' + str(round(((secondselapsed / sharedone) - secondselapsed) / 3600, 2)) + " hours."
