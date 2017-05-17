import json
from bs4 import BeautifulSoup
import gluon.contrib.simplejson
import os
import xmltodict
from bs4 import CData

def call():
    session.forget()
    return service()

web2py_path = os.path.dirname(os.path.abspath('__file__'))

@service.json
def book_chapters():

    tree = []

    xml = open('{}/{}'.format(web2py_path, 'applications/HEIDIEditor/static/WysiwigEditor/data/bookSample.xml'))

    soup = BeautifulSoup(xml, 'xml', from_encoding='utf-8')
    partflag = False;
    book = {
        'text': soup.find('book-id').text,
        'id': soup.find('book-id').text,
        'state': {
            'opened': True,
            'selected': True
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
            part['state'] = {'opened': True, 'selected': False, 'disabled': True}
            part['type'] = 'part'
            part['parent'] = book['id']
            tree.append(part)
        elif str(i['book-part-type']) == unicode('chapter'):
            chapter = {}
            chapter['text'] = i['id']
            chapter['id'] = i['id']
            chapter['state'] = {'opened': False, 'selected': False}
            chapter['type'] = 'chapter'
            if partflag:
                parent = i.find_parent('book-part')
                if (parent is not None) and (parent['book-part-type'] == unicode('part')):
                    chapter['parent'] = parent['id']
            else:
                chapter['parent'] = book['id']
            tree.append(chapter)

    return tree


@service.json
def bookJson():
    def validate(dic):
        if dic['book']['book-meta'].has_key('contrib-group'):
            if not (isinstance(dic['book']['book-meta']['contrib-group']['contrib'], list)):
                dic['book']['book-meta']['contrib-group']['contrib'] = [
                    dic['book']['book-meta']['contrib-group']['contrib']]
        else:
            dic['book']['book-meta']['contrib-group'] = {'contrib': []}

        if dic['book']['book-meta'].has_key('contrib-group'):
            if not (isinstance(dic['book']['book-meta']['aff'], list)):
                dic['book']['book-meta']['aff'] = [dic['book']['book-meta']['aff']]
        else:
            dic['book']['book-meta']['aff'] = []

        return dic

    def escape(xml):
        soup = BeautifulSoup(xml, 'xml', from_encoding='utf-8')
        italic_tag = soup.italic
        italic_tag.name = 'i'
        for i in soup.find_all('p'):
            parent = i.parent
            if parent is not None:
                string = ''.join([str(j) for j in parent.contents])
                cdata = CData(string)
                new_p = soup.new_tag('p')
                new_p.string = cdata
                parent.clear()
                parent.append(new_p)
        return str(soup)

    xml = open('{}/{}'.format(web2py_path, 'applications/HEIDIEditor/static/WysiwigEditor/data/bookSample.xml'))
    xmldata = escape(xml)
    xmldict = xmltodict.parse(xmldata)
    jsondata = validate(xmldict)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return jsondata
