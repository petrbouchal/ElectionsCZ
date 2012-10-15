'''
Created on Apr 1, 2012

@author: petrbouchal
'''

from lxml import html
from lxml import etree
import lxml

parser = etree.HTMLParser()
tree   = etree.parse(StringIO('http://www.google.com'), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")