#!/usr/bin/python

from glob import glob
# import logging
import os, sys
from xml2json import xml2json
import optparse
import json




def run(upload_dir):
    uploads = glob(upload_dir+'/*.*')
    # print uploads

    for u in uploads:
        filename = u.split('.',1)
        # print filename
        if not filename[1] in ['doc', 'docx', 'odt']: break

        # stdin options
        argv =
        meTypeset.main()

        basename = filename[0].split('/')
        nlmfile = upload_dir+"/out/nlm/"+basename[-1]+".xml"
        xmldata = open(nlmfile).read()
        options = optparse.Values({'pretty': False})
        jsondata = xml2json(xmldata, options, 1)
        # print jsondata

        jsonfile = upload_dir+"/out/"+basename[-1]+".json"
        with open(jsonfile, 'wb') as f:
            json.dump(jsondata, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    sys.path.append("/home/m1o/git/meTypeset/bin")
    import meTypeset
    UPLOAD_DIR = '/var/www/html/HEIDIEditor/html/files'
    run(UPLOAD_DIR)

    # jump to next page
    # print open("step3.html", "r").read()