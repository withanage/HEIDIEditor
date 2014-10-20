#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import xmltodict
from bs4 import BeautifulSoup
from bs4 import CData


def validate(dic):
    if dic['book']['book-meta'].has_key('contrib-group'):
        if not(isinstance(dic['book']['book-meta']['contrib-group']['contrib'], list)):
            dic['book']['book-meta']['contrib-group']['contrib'] = [dic['book']['book-meta']['contrib-group']['contrib']]
    else:
        dic['book']['book-meta']['contrib-group'] = {'contrib': []}

    if dic['book']['book-meta'].has_key('contrib-group'):
        if not(isinstance(dic['book']['book-meta']['aff'], list)):
            dic['book']['book-meta']['aff'] = [dic['book']['book-meta']['aff']]
    else:
        dic['book']['book-meta']['aff'] = []

    return dic

def escape(xml):
    soup = BeautifulSoup(xml, 'xml', from_encoding='utf-8')
    for i in soup.find_all('p'):
        if i.string is None:
            string = ''.join([str(j) for j in i.contents])
            cdata = CData(string)
            i.string = ''
            i.string.replace_with(cdata)
    return str(soup)

def getjson(xmldata):
    xmldata = escape(xmldata)
    return xmltodict.parse(xmldata)

if __name__ == "__main__":
    xml = open('../data/bookSample.xml').read()
    xmldict = getjson(xml)
    jsondata = validate(xmldict)

    print "Content-type: application/json\n\n"
    print json.JSONEncoder().encode(jsondata)
    print