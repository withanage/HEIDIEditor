#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from bisect import insort_right

UPLOAD_DIR = '../html/files'

book =  {
    'text': '',
    'state': {
        'opened' : True,
        'selected' : True
    },
    'children' : []
}

for i in os.listdir(UPLOAD_DIR):
    basename, ext = os.path.splitext(i)
    if ext in ['.doc', '.docx', '.odt']:
        bookname, filename = basename.split('_', 1)
        book['text'] = bookname
        insort_right(book['children'], filename+ext)


print "Content-type: application/json\n\n"
print("[" + json.JSONEncoder().encode(book) + "]\n")