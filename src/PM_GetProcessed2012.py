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
from datetime import datetime

csvout = './CSVKraje/Kraje_Processing_Realtime2012.csv'
tracker = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = []
writer.writerow(headerrow)

while(1 == 1):
    cas = datetime.strftime(datetime.now(), '%d-%m%Y_%H-%M-%S')
    filenameA = "ProcessingFiles/krajeprocessing_1_" + cas + ".html"
    filenameB = "ProcessingFiles/krajeprocessing_2_" + cas + ".html"
    try:
        souborA = urllib2.urlopen('http://volby.cz/pls/kz2012/kz71?xjazyk=CZ&xdatum=20121012&xnumnuts=0&xv=0')
    except IOError:
        try:
            souborA = urllib2.urlopen('http://volby.cz/pls/kz2012/kz71?xjazyk=CZ&xdatum=20121012&xnumnuts=0&xv=0')
        except IOError:
            continue
    try:
        souborB = urllib2.urlopen('http://volby.cz/pls/kz2012/kz71?xjazyk=CZ&xdatum=20121012&xnumnuts=0&xv=1')
    except IOError:
        try:
            souborB = urllib2.urlopen('http://volby.cz/pls/kz2012/kz71?xjazyk=CZ&xdatum=20121012&xnumnuts=0&xv=1')
        except IOError:
            continue
    htmlA = souborA.read()
    htmlB = souborB.read()
    nadobaA = open(filenameA, "wb")
    nadobaB = open(filenameB, "wb")
    nadobaA.write(htmlA)
    nadobaB.write(htmlB)
    print "Saved 2 files:"
    print filenameA
    print filenameB
    nadobaA.close()
    nadobaB.close()

    html = souborA.replace('content="text/html;', 'content="text/html"')
    soup = BeautifulSoup(html, "lxml")

    krajelist = soup.find_all("td", { "headers" : "sa1" })
    okresylist = soup.find_all("td", {"headers": ""})
    for kraj in krajelist:
        pocetradek = kraj.rowspan[0]
        print pocetradek



    for i in range(0, 30):
        print "waiting 10 seconds",
        for i in range(0, 9):
            time.sleep(1)
            print("."),
        time.sleep(1)
        print (".")
    print "5 minutes elapsed, downloading"
    writer.writerow(row)

