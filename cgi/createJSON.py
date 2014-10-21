#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import xmltodict

UPLOAD_DIR = '../html/uploads'
METADATA_NAME = 'metadata.xml'
PUBLISHER_NAME = 'Heidelberg University Press'
PUBLISHER_LOC = 'Heidelberg'

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


def validate(xmldict):
    if(xmldict['tagset'] == 'article'):
        if not(xmldict['article']['front']['journal-meta'].has_key('publisher')):
            mldict['article']['front']['journal-meta']['publisher'] = {'publisher-name' : PUBLISHER_NAME, 'publisher-loc': PUBLISHER_LOC}
        if not(xmldict['article']['front']['journal-meta'].has_key('journal-title-group')):
            if (isinstance(xmldict['article']['front']['journal-meta']['journal-id'], str)):
                xmldict['article']['front']['journal-meta']['journal-id'] = {'@pub-type': 'epub', '#text': xmldict['article']['front']['journal-meta']['journal-id']}
            xmldict['article']['front']['journal-meta']['journal-title-group'] = {'journal-title': xmldict['article']['front']['journal-meta']['journal-id']['#text']}
        if(xmldict['article']['front']['article-meta'].has_key('contrib-group')):
            if not(isinstance(xmldict['article']['front']['article-meta']['contrib-group'], list)):
                xmldict['article']['front']['article-meta']['contrib-group'] = [xmldict['article']['front']['article-meta']['contrib-group']]
    elif(mxldict['tagset'] == 'book'):
        if(xmldict['book']['book-meta'].has_key('contrib-group')):
            if not(isinstance(xmldict['book']['book-meta']['contrib-group'], list)):
                xmldict['book']['book-meta']['contrib-group'] = [xmldict['book']['book-meta']['contrib-group']]
    return xmldict



for root, dirs, files in os.walk(UPLOAD_DIR):
    if(METADATA_NAME in files):
        xmldata = open(root+"/"+METADATA_NAME).read()
        xmldict = xmltodict.parse(xmldata)
        tagset = predictTagset(xmldict)
        xmldict['tagset'] = tagset
        xmldict['id'] = root.split('/')[-1]
        xmldict[tagset] = xmldict['metadata']
        del xmldict['metadata']
        xmldict = validate(xmldict)
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
            xmldict = validate(xmldict)
            jsondata.append(xmldict)
        break


#with open('test.json', 'w+') as f:
#    json.dump(jsondata, f, sort_keys=False, indent=4)

print "Content-type: application/json\n\n"
print json.JSONEncoder().encode(jsondata)
print