#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
#import pprint
from bs4 import BeautifulSoup


tree =  []


xml = open('../data/bookSample.xml')
soup = BeautifulSoup(xml, 'xml', from_encoding='utf-8')
partflag = False;
book = {
    'text': soup.find('book-id').text,
    'id': soup.find('book-id').text,
    'state': {
        'opened' : True,
        'selected' : True
    },
    'type': 'book',
    'parent': '#'
}
tree.append(book)

for i in soup.find_all('book-part'):
    if str(i['book-part-type']) == unicode('part'):
        partflag = True;
        part = {}
        part['text'] = i['id']
        part['id'] = i['id']
        part['state'] = {'opened' : True, 'selected' : False}
        part['type'] = 'part'
        part['parent'] = book['id']
        tree.append(part)
    elif str(i['book-part-type']) == unicode('chapter'):
        chapter = {}
        chapter['text'] = i['id']
        chapter['id'] = i['id']
        chapter['state'] = {'opened' : False, 'selected' : False}
        chapter['type'] = 'chapter'
        if partflag:
            parent = i.find_parent('book-part')
            if (parent is not None) and (parent['book-part-type'] == unicode('part')):
                chapter['parent'] = parent['id']
        else:
            chapter['parent'] = book['id']
        tree.append(chapter)

#pprint.pprint(tree)



print "Content-type: application/json\n\n"
print(json.JSONEncoder().encode(tree) + "\n")