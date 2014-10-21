#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from bisect import insort_right

UPLOAD_DIR = '../html/files'

book =  [{
    'text': '',
    'id': '',
    'state': {
        'opened' : True,
        'selected' : True
    },
    'type': 'book',
    'parent': '#'
}]

for i in os.listdir(UPLOAD_DIR):
    basename, ext = os.path.splitext(i)
    if ext in ['.doc', '.docx', '.odt']:
        bookname, filename = basename.split('_', 1)
        book[0]['text'] = bookname
        book[0]['id'] = bookname
        book.append({'id':filename, 'text':filename+ext, 'type':'file', 'state':{'opened':False, 'selected':False}, 'parent': bookname})


print "Content-type: application/json\n\n"
print(json.JSONEncoder().encode(book) + "\n")