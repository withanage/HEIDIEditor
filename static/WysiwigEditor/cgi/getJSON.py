#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

FILE_PATH = '../data/out.json'

f = open(FILE_PATH, 'w+')
jsondata = json.load(f)
f.close()

print "Content-type: application/json\n\n"
print json.JSONEncoder().encode(jsondata)
print