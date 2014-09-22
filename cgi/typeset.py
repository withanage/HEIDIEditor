#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
import os, sys
from xml2json import xml2json
import optparse
import json

cgitb.enable()

def run(upload_dir, metadata_path):
    uploads = os.listdir(upload_dir)
    # print uploads

    for item in uploads:
        filename = item.split('.',1)
        if not filename[1] in ['doc', 'docx', 'odt']: break

        # stdin options
        out_dir = upload_dir+"/out_"+filename[0]
        # opt = filename[1] + " " + upload_dir + "/" + item + " " + out_dir + " -d -m " + metadata_path
        opt = filename[1] + " " + upload_dir + "/" + item + " " + out_dir
        # print opt
        meTypeset.test(opt)

        nlmfile = out_dir+"/nlm/out.xml"
        xmldata = open(nlmfile).read()
        options = optparse.Values({'pretty': True})
        jsondata = xml2json(xmldata, options, 1)
        # print jsondata

        jsonfile = out_dir+".json"
        with open(jsonfile, 'wb') as f:
            json.dump("["+jsondata+"]", f, sort_keys=False, indent=4)


if __name__ == "__main__":
    sys.path.append("../meTypeset/bin")
    import meTypeset
    UPLOAD_DIR = '../html/files'
    METADATA_PATH = '../meTypeset/metadata/metadata.xml'
    run(UPLOAD_DIR, METADATA_PATH)

    # jump to next page
    print "Location: http://kjc-sv003.kjc.uni-heidelberg.de/HEIDIEditor/html/step2.html"
    print