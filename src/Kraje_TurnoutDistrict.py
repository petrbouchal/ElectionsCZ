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

csvout = './CSVKraje/Kraje_TurnoutDistrict.csv'

strany = open(csvout, 'wb')
writer = csv.writer(strany)
headerrow = ['Kraj', 'Okres', 'KrajNazev', 'OkresNazev', 'Okrsky', 'Volici', 'Vydane', 'Ucast', 'Odevzdane', 'Platne', 'PlatneProc', 'URL']
writer.writerow(headerrow)

for okres in krajokres:
    urldat = 'http://volby.cz/pls/kz2008/kz311?xjazyk=CZ&xdatum=20081017&xkraj=' + str(okres[0]) + '&xnumnuts=' + str(okres[1])
    # make an exception url for Prague:
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
    
    okrsky = soup.find_all("td", { "headers" : "sua1 sub1" })
    volici = soup.find_all("td", { "headers" : "sua2" })
    vydane = soup.find_all("td", { "headers" : "sua3" })
    ucast = soup.find_all("td", { "headers" : "sua4" })
    odevzdane = soup.find_all("td", { "headers" : "sua5" })
    platne = soup.find_all("td", { "headers" : "sua6" })
    platneProc = soup.find_all("td", { "headers" : "sua7" })
    if len(odevzdane) != 0:
        okrskyB = okrsky[0].contents
        voliciB = volici[0].contents
        vydaneB = vydane[0].contents
        ucastB = ucast[0].contents
        odevzdaneB = odevzdane[0].contents                        
        platneB = platne[0].contents
        platneProcB = platneProc[0].contents
        okrskyA = okrskyB[0].replace(u' ',u'').replace(u'\xa0',u'')
        voliciA = voliciB[0].replace(u' ',u'').replace(u'\xa0',u'')
        vydaneA = vydaneB[0].replace(u' ',u'').replace(u'\xa0',u'')
        ucastA = ucastB[0].replace(u' ',u'').replace(u'\xa0',u'')
        odevzdaneA = odevzdaneB[0].replace(u' ',u'').replace(u'\xa0',u'')         
        platneA = platneB[0].replace(u' ',u'').replace(u'\xa0',u'')
        platneProcA = platneProcB[0].replace(u' ',u'').replace(u'\xa0',u'').replace('&nbsp;','').replace(',','.')
        row = [okres[0], okres[1], krajname, okresname, okrskyA, voliciA, vydaneA, ucastA, odevzdaneA, platneA, platneProcA, urldat]
        writer.writerow(row)