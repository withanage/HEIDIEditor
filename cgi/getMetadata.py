#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import xmltodict

UPLOAD_DIR = '../html/uploads'
METADATA_NAME = 'metadata.xml'

jsondata = {'metadata': None}
for root, dirs, files in os.walk(UPLOAD_DIR):
    if(METADATA_NAME in files):
        xmldata = open(root+"/"+METADATA_NAME).read()
        jsondata = xmltodict.parse(xmldata)
        break


print "Content-type: application/json\n\n"
print json.JSONEncoder().encode(jsondata)+"\n"