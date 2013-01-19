'''
Created on Jan 12, 2013

@author: petrbouchal
'''
from bs4 import BeautifulSoup
# import re
import urllib2
import csv
import time
from datetime import datetime
import sys

print sys.getdefaultencoding()

url = 'http://volby.cz/pls/prez2013/pe51?xjazyk=CZ&xnumnuts=0&xv=21'

csvout = '../data-votes/PR2013/Pres_ZpracovaniLive.csv'
kandidati = open(csvout, 'ab', 0)
writer = csv.writer(kandidati)
headerrow = ['Kraj', 'Okres', 'Kod', 'Nazev', 'Zpracovano', 'Nezpracovano',
             "URLfrom", "UrlMisto"]
writer.writerow(headerrow)

while(1 == 1):
    cas = datetime.strftime(datetime.now(), '%Y-%d-%m-T%H:%M:%S')
    try:
        response = urllib2.urlopen(url)
    except IOError:
        print("Opening url" + url + "failed, trying again.")
        try:
            response = urllib2.urlopen(url)
        except IOError:
            print("Second try failed, aborting")
            continue
    html0 = response.read()
    html = html0.replace('content="text/html;', 'content="text/html"')
    soup = BeautifulSoup(html, "lxml")

    kraje = soup.find_all("td", {"headers" : "sa1"})
    okresy = soup.find_all("td", {"headers" : "sa2"})
    mistanazvy = soup.find_all("td", {"headers" : "sa3 sb2"})
    mistakody = soup.find_all("td", {"headers" : "sa3 sb1"}) # note this is <a>
    mistanezprac = soup.find_all("td", {"headers" : "sa5"})
    mistazprac = soup.find_all("td", {"headers" : "sa4"})

    countmistovkraji = 0
    countmistovokrese = 0
    krajthrough = 0
    okresthrough = 0

    for i in range(len(mistanazvy)):
        countmistovkraji += 1
        countmistovokrese += 1

        mistourl = mistakody[i].a['href']
        mistokod = mistakody[i].a.contents[0]
        mistonazev = mistanazvy[i].contents[0]
        mistozprac = mistazprac[i].contents[0]
        mistonezprac = mistanezprac[i].contents[0]

        if countmistovkraji - 1 == len(range(int(kraje[krajthrough]['rowspan']))):
            krajthrough += 1
            countmistovkraji = 0
        kraj = kraje[krajthrough].contents[0]
        if countmistovokrese - 1 == len(range(int(okresy[okresthrough]['rowspan']))):
            okresthrough += 1
            countmistovokrese = 0
        okres = okresy[okresthrough].contents[0]
        row = [kraj, okres, mistokod, mistonazev, mistozprac, mistonezprac,
             url, mistourl, cas]
        print row
        writer.writerow(row)

    for i in range(0, 30):
        print "waiting 10 seconds",
        for i in range(0, 9):
            time.sleep(1)
            print("."),
        time.sleep(1)
        print (".")
    print "5 minutes elapsed, downloading"





