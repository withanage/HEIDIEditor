#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
import logging
import os
import time
from datetime import datetime
import sys
from xml2json import xml2json
import optparse
import json
import shutil

cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='typeset.log')

def typeset(item, upload_dir, metadata_path):
    itemname = os.path.split(item)[-1]
    logging.info("\t"+str(datetime.now().time())+":\t Checking validation "+itemname+" ...")
    if not os.path.isfile(upload_dir+"/"+item):
        logging.debug("\t"+str(datetime.now().time())+":\t Path error: "+upload_dir+"/"+itemname)
        return
    filename = itemname.split('.',1)
    if len(filename) != 2:
        logging.debug("\t"+str(datetime.now().time())+":\t Filename error: "+upload_dir+"/"+itemname)
        return
    if not filename[1] in ['doc', 'docx', 'odt']:
        logging.debug("\t"+str(datetime.now().time())+":\t Filetype error: "+ upload_dir+"/"+itemname)
        return

    out_dir = upload_dir+"/out_"+filename[0]
    if os.path.exists(out_dir):
        logging.debug("\t"+str(datetime.now().time())+":\t "+out_dir+" already exists. remove it.")
        shutil.rmtree(out_dir)
    opt = filename[1] + " " + upload_dir + "/" + itemname + " " + out_dir + " -d -m " + metadata_path
    logging.info("\t"+str(datetime.now().time())+":\t meTypeset.py "+opt)
    log = meTypeset.test(opt)
    logging.info("\t"+str(datetime.now().time())+":\t meTypeset debug log \n"+log)
    
    logging.info("\t"+str(datetime.now().time())+":\t Generating JSON ...")
    nlmfile = out_dir+"/nlm/out.xml"
    xmldata = open(nlmfile).read()
    options = optparse.Values({'pretty': True})
    jsondata = xml2json(xmldata, options, 1)
    # logging.info("\t"+str(datetime.now().time())+":\t JSON data: \n"+jsondata)

    jsonfile = "../html/json/"+filename[0]+".json"
    if os.path.exists(jsonfile):
        logging.debug("\t"+str(datetime.now().time())+":\t "+jsonfile+" already exists. remove it.")
        os.remove(jsonfile)
    logging.info("\t"+str(datetime.now().time())+":\t Writing JSON to "+jsonfile+" ...")
    with open(jsonfile, 'w+') as f:
        json.dump("["+jsondata+"]", f, sort_keys=False, indent=4)

    xmlfile = "../html/xml/"+filename[0]+".xml"
    if os.path.exists(xmlfile):
        logging.debug("\t"+str(datetime.now().time())+":\t "+xmlfile+" already exists. remove it.")
        os.remove(xmlfile)
    logging.info("\t"+str(datetime.now().time())+":\t Copying XML to "+xmlfile+" ...")
    shutil.copyfile(nlmfile, xmlfile)


if __name__ == "__main__":
    logging.info("================run typeset.py "+str(datetime.now())+"=================")
    sys.path.append("../meTypeset/bin")
    import meTypeset
    UPLOAD_DIR = '../html/files'
    METADATA_PATH = os.path.abspath('../html/xml/metadataTest.xml')

    if (len(sys.argv) == 2):
        typeset(os.path.split(sys.argv[1])[-1], UPLOAD_DIR, METADATA_PATH)

    else:
        before = dict([(f, None) for f in os.listdir(UPLOAD_DIR)])
        while 1:
            time.sleep(1)
            logging.info("\t"+str(datetime.now().time())+":\t Observing upload folder"+UPLOAD_DIR+" ...")
            after = dict([(f, None) for f in os.listdir(UPLOAD_DIR)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                for item in added:
                    typeset(item, UPLOAD_DIR, METADATA_PATH)

            if removed:
                for item in removed:
                    filename = item.split('.',1)
                    out_dir = UPLOAD_DIR+"/out_"+filename[0]
                    if os.path.exists(out_dir):
                        logging.info("\t"+str(datetime.now().time())+":\t Removing "+ out_dir +" ...")
                        shutil.rmtree(out_dir)
                    jsonfile = "../html/json/"+filename[0]+".json"
                    if os.path.exists(jsonfile):
                        logging.info("\t"+str(datetime.now().time())+":\t Removing "+jsonfile+" ...")
                        os.remove(jsonfile)
                    xmlfile = "../html/xml/"+filename[0]+".xml"
                    if os.path.exists(xmlfile):
                        logging.info("\t"+strq(datetime.now().time())+":\t Removing "+xmlfile+" ...")
                        os.remove(xmlfile)

            before = after