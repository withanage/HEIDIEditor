#!/usr/local/bin/python

import cgi
import os

#print "uploading..."

form = cgi.FileStorage()
if form.has_key('file'):
    item = form['file']
    if item.file:
        outFile = file(os.path.join('../files', item.filename), 'wb')
        while True:
            chunk = item.file.read(2000000)
            if not chunk:
                break
            outFile.write(chunk)
        outFile.close()
        result = 1


#if (result == 1):
#    print "uploaded successfully"
#else:
#    print "faild to upload"