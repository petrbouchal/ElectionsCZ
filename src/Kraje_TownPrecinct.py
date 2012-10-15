# Import the BeautifulSoup HTML parser
from bs4 import BeautifulSoup
# Import the regular expression module
import re
# Import module to open webpages
import urllib2
# Import module to write csv files
import csv

electyear = str(2012)
electdatestring = str(20121012)
electtype = "Kraj"

csvout = './CSVKraje/Kraje_TownPrecinctData_' + electtype + '_' + electyear + '.csv'
obcecsv = open(csvout, 'wb')
writer = csv.writer(obcecsv)
urlfront = 'http://www.volby.cz/pls/kz' + electyear + '/kz81?xjazyk=CZ&xdatum=' + electdatestring

webseznam = urllib2.urlopen(urlfront)
html = webseznam.read()
soup = BeautifulSoup(html, "html.parser")
bunkasurl = soup.find_all("td", { "class" : "center", "colspan" : None})

towncounter = 0

for bunka in range(len(bunkasurl)):
    aa = re.compile('xnumnuts=[0-9]{4}')
    blah = str(bunkasurl[bunka])
    kod = aa.findall(blah)
    kodokresu = kod[0].replace('xnumnuts=', '')
    bb = re.compile('xkraj=[0-9]{1,2}')
    kraj = bb.findall(blah)
    cislokraje = kraj[0].replace('xkraj=', '')
    for kus in kod:
        urldat = 'http://www.volby.cz/pls/kz' + electyear + '/kz811?xjazyk=CZ&xdatum=' + electdatestring + '&xkraj=' + cislokraje + '&xnumnuts=' + kodokresu
        print urldat
        response = urllib2.urlopen(urldat)
        html0 = response.read()
        html = html0.replace('content="text/html;', 'content="text/html"')
        soup = BeautifulSoup(html, "lxml")

        cisloobce1 = soup.find_all("td", { "headers" : "t1sa1 t1sb1" })
        cisloobce2 = soup.find_all("td", { "headers" : "t2sa1 t2sb1" })
        cisloobce3 = soup.find_all("td", { "headers" : "t3sa1 t3sb1" })

        cisloobce = cisloobce1 + cisloobce2 + cisloobce3

        nazevobce1 = soup.find_all("td", { "headers" : "t1sa1 t1sb2" })
        nazevobce2 = soup.find_all("td", { "headers" : "t2sa1 t2sb2" })
        nazevobce3 = soup.find_all("td", { "headers" : "t3sa1 t3sb2" })

        nazevobce = nazevobce1 + nazevobce2 + nazevobce3

        krajraw = re.findall('[Kraj:]{5}.*?\n', str(soup), flags=re.DOTALL)
        nazevkraje = krajraw[0].replace('Kraj: ', '').encode('utf-8', 'replace').replace('</h3>', '')

        kodkraje = kodokresu[0] + kodokresu[1]

        pocetokrsku1 = soup.find_all("td", { "headers" : "t1sa2" })
        pocetokrsku2 = soup.find_all("td", { "headers" : "t2sa2" })
        pocetokrsku3 = soup.find_all("td", { "headers" : "t3sa2" })
        pocetokrsku = pocetokrsku1 + pocetokrsku2 + pocetokrsku3

        for kousek in range(len(cisloobce)):
            cisloA = cisloobce[kousek].contents[0]
            nazevA = nazevobce[kousek].contents[0]
            pocetA = pocetokrsku[kousek].contents[0]
            row = [cisloA, nazevA.encode('utf-8', 'replace'), pocetA, cislokraje, kodokresu, kodkraje, nazevkraje, urldat]
            if cisloA != '-':
                writer.writerow(row)

                towncounter += 1

        print 'Collected data on ' + str(towncounter) + ' municipalities.'
