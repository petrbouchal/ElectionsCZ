# Import the BeautifulSoup HTML parser
from bs4 import BeautifulSoup
# Import the regular expression module
import re
# Import module to open webpages
import urllib2
# Import module to write csv files
import csv

csvout = './CSVPS/PS_TownPrecinctData.csv'
obcecsv = open(csvout, 'wb')
writer = csv.writer(obcecsv)

webseznam = urllib2.urlopen('http://www.volby.cz/pls/ps2010/ps81?xjazyk=CZ')
html = webseznam.read()
soupA = BeautifulSoup(html, "html.parser")
# prettysoup = soupA.prettify()
bunkasurl = soupA.findAll("td", { "class" : "center"})

for bunka in range(len(bunkasurl)):
    aa=re.compile('xnumnuts=[0-9]{4}')
    blah = str(bunkasurl[bunka])
    kod=aa.findall(blah)
    kodokresu = kod[0].replace('xnumnuts=','')
    for kus in kod:
        urldat = 'http://www.volby.cz/pls/ps2010/ps811?xjazyk=CZ&xnumnuts=' + kodokresu
        print urldat
        response = urllib2.urlopen(urldat)
        html0 = response.read()
        html = html0.replace('content="text/html;','content="text/html"')
        soup = BeautifulSoup(html, "lxml")
        # prettysoup = soup.prettify()
        cisloobce = soup.find_all("td", { "headers" : "t1sa1 t1sb1" })
        nazevobce = soup.find_all("td", { "headers" : "t1sa1 t1sb2" })
        pocetokrsku = soup.find_all("td", { "headers" : "t1sa2" })
        
        cisloobce2 = soup.find_all("td", { "headers" : "t2sa1 t2sb1" })
        nazevobce2 = soup.find_all("td", { "headers" : "t2sa1 t2sb2" })
        pocetokrsku2 = soup.find_all("td", { "headers" : "t2sa2" })

        cisloobce3 = soup.find_all("td", { "headers" : "t3sa1 t3sb1" })
        nazevobce3 = soup.find_all("td", { "headers" : "t3sa1 t3sb2" })
        pocetokrsku3 = soup.find_all("td", { "headers" : "t3sa2" })
        
        cisloobce.extend(cisloobce2)
        nazevobce.extend(nazevobce2)
        pocetokrsku.extend(pocetokrsku2)
        
        cisloobce.extend(cisloobce3)
        nazevobce.extend(nazevobce3)
        pocetokrsku.extend(pocetokrsku3)
        
        krajraw = re.findall('[Kraj:]{5}.*?\n', str(soup), flags=re.DOTALL)
        nazevkraje = krajraw[0].replace('Kraj: ','').encode('utf-8','replace')
        
        kodkraje = kodokresu[0] + kodokresu[1]
        cislokraje = kodkraje.replace('11','1').replace('21','2').replace('31','3').replace('32','4').replace('41','5').replace('42','6').replace('51','7').replace('52','8').replace('53','9').replace('61','10').replace('62','11').replace('71','12').replace('72','13').replace('81','14')
                             
        for kousek in range(len(cisloobce)):
            cisloA = cisloobce[kousek].contents
            nazevA = nazevobce[kousek].contents
            pocetA = pocetokrsku[kousek].contents
            row = [cisloA[0], nazevA[0].encode('utf-8','replace'), pocetA[0], cislokraje, kodokresu, kodkraje, nazevkraje, urldat]
            if cisloA[0] != '-':                
                writer.writerow(row)
            
        
