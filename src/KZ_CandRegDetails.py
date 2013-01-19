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
import sys

print sys.getdefaultencoding()

## SET PARAMETERS
electyear = 2008
electtype = 'kz' # 'kz', 'ps', or 'oz'
pocetkandidatek = 100
vsechnykraje = range(1, 14)
votetype = 'Hlasy' # can be "Hlasy", "PrefHlasy" or "Ucast"
unitobs = 'KandidatKraj' # specify unit of observation and unit of aggregation

electyr = str(electyear)
electyrshrt = str(electyr[2]) + str(electyr[3])
electdatestring = electyr + str('1017')

csvout = '../data-votes/' + electtype + electyr + '/' \
+ electtype + electyrshrt + '_' + votetype + '_' + unitobs + '.csv'
outfile = open(csvout, 'wb')
writer = csv.writer(outfile)
headerrow = ['Kraj', 'Kandidatka', 'PoradiKand', 'KandJmeno', 'KandJmenoPrijmeni', \
             'KandKrestniJmeno', 'KandTitul', 'Povolani', 'Bydliste', 'KandVek', \
             'Hlasy', 'Procenta', 'Mandat', 'PoradiVysl', 'Prislusnost', \
             'NavrhujiciStrana', 'URL']
writer.writerow(headerrow)

vsechnykandidatky = range(1, pocetkandidatek + 1)
for partaj in vsechnykandidatky:
    for kraj in vsechnykraje:
        urldat = 'http://volby.cz/pls/kz' + electyr + '/kz111?xjazyk=CZ&xdatum=' + \
        electdatestring + '&xkraj=' + str(kraj) + '&xstrana=' + str(partaj) + '&xv=1&xt=1'
        print urldat
        print 'Strana: ' + str(partaj)
        print "Kraj: " + str(kraj)
        response = urllib2.urlopen(urldat)
        html0 = response.read()
        html = html0.replace('content="text/html;', 'content="text/html"')
        soup = BeautifulSoup(html, "lxml")
        #pick up data into lists
        poradiKand = soup.find_all("td", { "headers" : "sa3 sb5" })
        jmeno = soup.find_all("td", { "headers" : "sa3 sb6" })
        vek = soup.find_all("td", { "headers" : "sa3 sb7" })
        navrhStrana = soup.find_all("td", { "headers" : "sa4" })
        prislusnost = soup.find_all("td", { "headers" : "sa5" })
        hlasy = soup.find_all("td", { "headers" : "sa8 sb8" })
        procenta = soup.find_all("td", { "headers" : "sa8 sb9" })
        mandat = soup.find_all("td", { "headers" : "sa9" })
        poradiVysl = soup.find_all("td", { "headers" : "sa10" })
        bydliste = soup.find_all("td", { "headers" : "sa7" })
        povolani = soup.find_all("td", { "headers" : "sa6" })
        if len(poradiKand) != 0:
            for clovek in range(len(poradiKand)):
                poradiKandB = poradiKand[clovek].contents
                jmenoB = jmeno[clovek].contents
                vekB = vek[clovek].contents
                navrhStranaB = navrhStrana[clovek].contents
                prislusnostB = prislusnost[clovek].contents
                hlasyB = hlasy[clovek].contents
                procentaB = procenta[clovek].contents
                if len(poradiVysl) != 0:
                    poradiVyslB = poradiVysl[clovek].contents
                    mandatB = mandat[clovek].contents
                else:
                    poradiVyslB = ''
                    mandatB = ''
                povolaniB = povolani[clovek].contents
                bydlisteB = bydliste[clovek].contents
                # final cleanup
                poradiKandA = poradiKandB[0].strip()
                jmenoA = jmenoB[0].strip().encode('utf-8', 'replace')
                povolaniA = povolaniB[0].strip().encode('utf-8', 'replace')
                bydlisteA = bydlisteB[0].strip().encode('utf-8', 'replace')
                vekA = vekB[0].strip()
                hlasyX = hlasyB[0].strip()
                hlasyA = hlasyX.replace(u' ', u'').replace(u'\xa0', u'')
                procentaA = procentaB[0].strip().replace(',', '.')
                navrhStranaA = navrhStranaB[0].strip().encode('utf-8', 'replace')
                prislusnostA = prislusnostB[0].strip().encode('utf-8', 'replace')
                if len(poradiVyslB) != 0:
                    poradiVyslA = poradiVyslB[0].replace(u' ', u'').replace(u'\xa0', u'')
                    mandatX = mandatB[0].replace(u' ', u'').replace(u'\xa0', u'')
                    mandatA = mandatX.replace('*', '1').replace(u' ', u'').replace(u'\xa0', u'')
                    if mandatA == '':
                        mandatA = '0'
                else:
                    mandatA = 'NA'
                    poradiVyslA = 'NA'

                print jmenoA
                jmenolist = jmenoA.split("  ")
                if len(jmenolist) == 1:
                    jmenoprijmeni = jmenoA
                    titul = ""
                else:
                    jmenoprijmeni = jmenolist[0]
                    titul = jmenolist[1]

                krestnijmeno = jmenoprijmeni.split(" ")[-1]

                row = [kraj, partaj, poradiKandA, jmenoA, jmenoprijmeni, \
                       krestnijmeno, titul, povolaniA, bydlisteA, vekA, \
                       hlasyA, procentaA, mandatA, poradiVyslA, prislusnostA, \
                       navrhStranaA, urldat]
                #writer.writerow(row)
