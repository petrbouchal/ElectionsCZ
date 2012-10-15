'''
Created on Mar 31, 2012

@author: petrbouchal
'''

from bs4 import BeautifulSoup
import urllib2

hello = BeautifulSoup(urllib2.urlopen('http://volby.cz/pls/ps2006/ps311?xjazyk=CZ&xkraj=1'), "lxml")
prettyhello = hello.prettify()
# print prettyhello

for link in hello.body.find_all('a'):
    print(link.get('href'),link.get_text())

for tabulka in hello.body.find('table'):
    tabulka2 = tabulka.find_next_sibling('table')
    for podtab in tabulka2.find_all('table'):
        if podtab:
            for tr in podtab.find_all('tr'):
                print type(tr)
                print type(tabulka)
                print type(podtab)
                print type(tr)
                if tr:
                    prvnisloupec = tr.find('td')
                    druhysloupec = prvnisloupec.find_next_sibling('td')
                    tretisloupec = druhysloupec.find_next_sibling('td')
                    ctvrtyskoupec = tretisloupec.find_next_sibling('td')
                    patysloupec = ctvrtyskoupec.find_next_sibling('td')
                    acko = patysloupec.a
                    print acko.href
                    
for link in hello.body.find_all('a'):
    print link.href