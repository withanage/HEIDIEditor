#!/usr/bin/python

import cgi, cgitb
import os
import logging

cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='log.txt')

def save_file(form_field, upload_dir):
    logging.debug("==========save_file==========")

    form = cgi.FieldStorage(
        fp=self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':self.headers['Content-Type'],
        }
    )
    logging.debug(form)

    if not form.has_key(form_field): return

    fileitem = form[form_field]
    if not fileitem.file: return
    fout = file(os.path.join(upload_dir, fileitem.filename), 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()



if __name__ == '__main__' :
    save_file('file', '../html/files');