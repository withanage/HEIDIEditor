#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import xmltodict

UPLOAD_DIR = '../html/uploads'
METADATA_NAME = 'metadata.xml'

jsondata = [{'selected': True, 'type': 'book'}]

def predictTagset(d):
    if(d.has_key('metadata')):
        if (d['metadata'].has_key('front')):
            return 'article'
        elif(d['metadata'].has_key('book-meta')):
            return 'book'
    elif(d.has_key('article')):
        return 'article'
    elif(d.has_key('book')):
        return 'book'
    else:
        return ''


for root, dirs, files in os.walk(UPLOAD_DIR):
    if(METADATA_NAME in files):
        xmldata = open(root+"/"+METADATA_NAME).read()
        xmldict = xmltodict.parse(xmldata)
        tagset = predictTagset(xmldict)
        xmldict['tagset'] = tagset
        xmldict['id'] = root.split('/')[-1]
        xmldict[tagset] = xmldict['metadata']
        del xmldict['metadata']
        jsondata[0].update(xmldict)

    if('xml' in dirs):
        xmlfiles = os.listdir(root+"/xml")
        for xml in xmlfiles:
            xmldata = open(root+"/xml/"+xml).read()
            xmldict = xmltodict.parse(xmldata)
            xmldict['selected'] = False
            xmldict['type'] = 'file'
            xmldict['tagset'] = predictTagset(xmldict)
            filename = os.path.splitext(xml)[0]
            xmldict['id'] = filename
            jsondata.append(xmldict)
        break


#with open('test.json', 'w+') as f:
#    json.dump(jsondata, f, sort_keys=False, indent=4)

print "Content-type: application/json\n\n"
print json.JSONEncoder().encode(jsondata)
print