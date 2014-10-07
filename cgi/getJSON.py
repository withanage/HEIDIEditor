#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import xmltodict

UPLOAD_DIR = '../html/uploads'
METADATA_NAME = 'metadata.xml'

jsondata = []

bookname = ''
bookdict = {}

for root, dirs, files in os.walk(UPLOAD_DIR):
    if(METADATA_NAME in files):
        xmldata = open(root+"/"+METADATA_NAME).read()
        bookdict = xmltodict.parse(xmldata)
        bookdict['selected'] = True
        bookdict['type'] = 'book'
        bookname = root.split('/')[-1]

    if('xml' in dirs):
        xmlfiles = os.listdir(root+"/xml")
        for xml in xmlfiles:
            xmldata = open(root+"/xml/"+xml).read()
            xmldict = xmltodict.parse(xmldata)
            xmldict['selected'] = False
            xmldict['type'] = 'file'
            filename = os.path.splitext(xml)[0]
            xmldict['id'] = filename
            jsondata.append(xmldict)
        break

bookdict['id'] = bookname
jsondata.append(bookdict)

#with open('test.json', 'w+') as f:
#    json.dump(jsondata, f, sort_keys=False, indent=4)

print "Content-type: application/json\n\n"
print json.JSONEncoder().encode(jsondata)
print