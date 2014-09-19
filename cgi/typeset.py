#!/usr/bin/python

import cgitb
import os, sys
from xml2json import xml2json
import optparse
import json

cgitb.enable()

def run(upload_dir, metadata_path):
    uploads = os.listdir(upload_dir)
    # print uploads

    for u in uploads:
        filename = u.split('.',1)
        # print filename
        if not filename[1] in ['doc', 'docx', 'odt']: break

        # stdin options
        out_dir = upload_dir+"/out"
        argv = filename[1]+" "+upload_dir+filename[0]+out_dir+" -m "+metadata_path
        meTypeset.main()
        # give stdin options

        nlmfile = out_dir+"/nlm/out.xml"
        xmldata = open(nlmfile).read()
        options = optparse.Values({'pretty': False})
        jsondata = xml2json(xmldata, options, 1)
        # print jsondata

        jsonfile = out_dir+".json"
        with open(jsonfile, 'wb') as f:
            json.dump("["+jsondata+"]", f, sort_keys=False, indent=4)


if __name__ == "__main__":
    sys.path.append("../meTypeset/bin")
    import meTypeset
    UPLOAD_DIR = '../html/files'
    METADATA_PATH = '.:/xml/metadataTest.xml'
    run(UPLOAD_DIR, METADATA_PATH)

    # jump to next page
    print "Location: http://" + os.environ['HTTP_HOST'] + "/HEIDIEditor/html/step2.html\n\n"