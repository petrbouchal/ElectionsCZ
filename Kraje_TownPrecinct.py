# Import the BeautifulSoup HTML parser
from bs4 import BeautifulSoup
# Import the regular expression module
import re
# Import module to open webpages
import urllib2
# Import module to write csv files
import csv

csvout = './CSVKraje/Kraje_TownPrecinctData.csv'
obcecsv = open(csvout, 'wb')
writer = csv.writer(obcecsv)

webseznam = urllib2.urlopen('http://www.volby.cz/pls/kz2008/kz81?xjazyk=CZ&xdatum=20081017')
html = webseznam.read()
soup = BeautifulSoup(html, "html.parser")
bunkasurl = soup.find_all("td", { "class" : "center", "colspan" : None})

for bunka in range(len(bunkasurl)):
    aa=re.compile('xnumnuts=[0-9]{4}')
    blah = str(bunkasurl[bunka])
    kod=aa.findall(blah)
    kodokresu = kod[0].replace('xnumnuts=','')
    bb=re.compile('xkraj=[0-9]{1,2}')
    kraj=bb.findall(blah)
    cislokraje = kraj[0].replace('xkraj=','')
    for kus in kod:
        urldat = 'http://www.volby.cz/pls/kz2008/kz811?xjazyk=CZ&xdatum=20081017&xkraj=' +  cislokraje + '&xnumnuts=' + kodokresu
        print urldat
        response = urllib2.urlopen(urldat)
        html0 = response.read()
        html = html0.replace('content="text/html;','content="text/html"')
        soup = BeautifulSoup(html, "lxml")
        prettysoup = soup.prettify()
        cisloobce = soup.find_all("td", { "class" : "center" })
        nazevobce = soup.find_all("td", { "class" : None })

        krajraw = re.findall('[Kraj:]{5}.*?\n', str(soup), flags=re.DOTALL)
        nazevkraje = krajraw[0].replace('Kraj: ','').encode('utf-8','replace')
        
        kodkraje = kodokresu[0] + kodokresu[1] 
        
        pocetokrsku = soup.find_all("td", { "class" : "cislo" }) 
        for kousek in range(len(cisloobce)):
            cisloA = cisloobce[kousek].contents
            nazevA = nazevobce[kousek].contents
            pocetA = pocetokrsku[kousek].contents
            row = [cisloA[0], nazevA[0].encode('utf-8','replace'), pocetA[0], cislokraje, kodokresu, kodkraje, nazevkraje, urldat]
            if cisloA != '-':
                writer.writerow(row)
            
        
