#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgitb
import logging
import os
import stat
import time
from datetime import datetime
import sys
import xmltodict
import optparse
import json
import shutil

cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='typeset.log')


#### Constant variables ####
TMP_DIR = '../html/files'
UPLOAD_DIR = '../html/uploads'
METADATA_PATH = os.path.abspath('../html/xml/metadataTest.xml')
PERM_666 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)


def typeset(item):
    bookname = item.split('_',1)
    logging.info("\t"+str(datetime.now().time())+":\t Checking validation "+item+" ...")
    if not os.path.isfile(TMP_DIR+"/"+item):
        logging.debug("\t"+str(datetime.now().time())+":\t Path error: "+item)
        return
    filename = os.path.splitext(bookname[1])
    if len(filename) != 2:
        logging.debug("\t"+str(datetime.now().time())+":\t Filename error: "+item)
        return
    if not filename[1] in ['.doc', '.docx', '.odt']:
        logging.debug("\t"+str(datetime.now().time())+":\t Filetype error: "+item)
        return

    bookname_dir = UPLOAD_DIR+"/"+bookname[0]
    out_dir = bookname_dir+"/"+"out_"+filename[0]
    if os.path.exists(out_dir):
        logging.debug("\t"+str(datetime.now().time())+":\t "+out_dir+" already exists. remove it.")
        shutil.rmtree(out_dir)
    opt = filename[1].strip('.') + " " + bookname_dir + "/" + bookname[1]  + " " + out_dir + " -d -m " + METADATA_PATH
    logging.info("\t"+str(datetime.now().time())+":\t [-------meTypeset-------]")
    logging.info("\t"+str(datetime.now().time())+":\t meTypeset.py "+opt)
    log = meTypeset.test(opt)
    logging.info("\t"+str(datetime.now().time())+":\t meTypeset debug log \n"+log)
    
    logging.info("\t"+str(datetime.now().time())+":\t Generating JSON ...")
    nlmfile = out_dir+"/"+"nlm"+"/"+"out.xml"
    xmldata = open(nlmfile).read()
    jsondata = xmltodict.parse(xmldata)
    # logging.info("\t"+str(datetime.now().time())+":\t JSON data: \n"+jsondata)

    if not os.path.isdir(bookname_dir+"/"+"json"):
        logging.info("\t"+str(datetime.now().time())+":\t Making directory "+bookname_dir+"/"+"json"+" ...")
        os.mkdir(bookname_dir+"/"+"json", 0775)
    jsonfile = bookname_dir+"/"+"json"+"/"+filename[0]+".json"
    if os.path.exists(jsonfile):
        logging.debug("\t"+str(datetime.now().time())+":\t "+jsonfile+" already exists. remove it.")
        os.remove(jsonfile)
    logging.info("\t"+str(datetime.now().time())+":\t Writing JSON to "+jsonfile+" ...")
    with open(jsonfile, 'w+') as f:
        json.dump(jsondata, f, sort_keys=False, indent=4)

    if not os.path.isdir(bookname_dir+"/"+"xml"):
        logging.info("\t"+str(datetime.now().time())+":\t Making directory "+bookname_dir+"/"+"xml"+" ...")
        os.mkdir(bookname_dir+"/"+"xml", 0775)
    xmlfile = bookname_dir+"/"+"xml"+"/"+filename[0]+".xml"
    if os.path.exists(xmlfile):
        logging.debug("\t"+str(datetime.now().time())+":\t "+xmlfile+" already exists. remove it.")
        os.remove(xmlfile)
    logging.info("\t"+str(datetime.now().time())+":\t Copying XML to "+xmlfile+" ...")
    shutil.copyfile(nlmfile, xmlfile)


if __name__ == "__main__":
    logging.info("================run typeset.py "+str(datetime.now())+"=================")
    sys.path.append('../../meTypeset/bin')
    import meTypeset


    if (len(sys.argv) == 2):
        typeset(os.path.split(sys.argv[1])[-1])

    else:
        before = dict([(f, None) for f in os.listdir(TMP_DIR)])
        while 1:
            time.sleep(1)
            logging.info("\t"+str(datetime.now().time())+":\t Observing upload folder"+TMP_DIR+" ...")
            after = dict([(f, None) for f in os.listdir(TMP_DIR)])
            added = [f for f in after if not f in before]
            removed = [f for f in before if not f in after]

            if added:
                logging.info("\t"+str(datetime.now().time())+":\t [-------Upload-------]")
                for item in added:
                    # Change permission
                    if(os.path.isdir(TMP_DIR+"/thumbnail")):
                        for i in os.listdir(TMP_DIR+"/thumbnail"):
                            logging.info("\t"+str(datetime.now().time())+":\t Changing permission for "+i+" ...")
                            f = os.open(TMP_DIR+"/thumbnail/"+i, os.O_RDONLY)
                            os.fchmod(f, PERM_666)
                            os.close(f)
                    # Make Directory
                    bookname = item.split('_',1)
                    bookname_dir = UPLOAD_DIR+"/"+bookname[0]
                    if not os.path.isdir(bookname_dir):
                        logging.info("\t"+str(datetime.now().time())+":\t Making directory "+bookname_dir+"/ ...")
                        os.mkdir(bookname_dir, 0775)
                    # Copy file
                    filename = os.path.splitext(bookname[1])
                    if(filename[1] in ['.doc', '.docx', '.odt']):
                        logging.info("\t"+str(datetime.now().time())+":\t Copying file to "+bookname_dir+"/"+bookname[1]+" ...")
                        shutil.copy2(TMP_DIR+"/"+item, bookname_dir+"/"+bookname[1])
                    else:
                        media_dir = bookname_dir+"/media"
                        if not os.path.exists(media_dir):
                            logging.info("\t"+str(datetime.now().time())+":\t Making directory "+media_dir+"/ ...")
                            os.mkdir(media_dir, 0775)
                        logging.info("\t"+str(datetime.now().time())+":\t Copying file to "+media_dir+"/"+bookname[1]+" ...")
                        shutil.copy2(TMP_DIR+"/"+item, media_dir+"/"+bookname[1])
                    # Call meTypeset
                    typeset(item)

            if removed:
                logging.info("\t"+str(datetime.now().time())+":\t [-------Delete-------]")
                for item in removed:
                    bookname = item.split('_',1)
                    filename = os.path.splitext(bookname[1])
                    if(filename[1] in ['.doc', '.docx', '.odt']):
                        bookname_dir = UPLOAD_DIR+"/"+bookname[0]
                        if os.path.exists(bookname_dir+"/"+bookname[1]):
                            logging.info("\t"+str(datetime.now().time())+":\t Removing "+ bookname_dir+"/"+bookname[1] +" ...")
                            os.remove(bookname_dir+"/"+bookname[1])
                        if(len(os.listdir(bookname_dir)) == 0):
                            logging.info("\t"+str(datetime.now().time())+":\t Removing "+ bookname_dir+"/ ...")
                            os.rmdir(bookname_dir)
                        media_dir = UPLOAD_DIR+"/"+bookname[0]+"/media"
                        if os.path.exists(media_dir+bookname[1]):
                            logging.info("\t"+str(datetime.now().time())+":\t Removing "+ Umedia_dir+"/"+bookname[1] +" ...")
                            os.remove(media_dir+"/"+bookname[1])
                        if(len(os.listdir(media_dir)) == 0):
                            logging.info("\t"+str(datetime.now().time())+":\t Removing "+ media_dir+"/ ...")
                            os.rmdir(media_dir)
                    out_dir = UPLOAD_DIR+"/"+bookname[0]+"/out_"+filename[0]
                    if os.path.exists(out_dir):
                        logging.info("\t"+str(datetime.now().time())+":\t Removing "+ out_dir +" ...")
                        shutil.rmtree(out_dir)
                    jsonfile = JSON_DIR+"/"+bookname[0]+"/"+filename[0]+".json"
                    if os.path.exists(jsonfile):
                        logging.info("\t"+str(datetime.now().time())+":\t Removing "+jsonfile+" ...")
                        os.remove(jsonfile)
                    xmlfile = XML_DIR+"/"+bookname[0]+"/"+filename[0]+".xml"
                    if os.path.exists(xmlfile):
                        logging.info("\t"+strq(datetime.now().time())+":\t Removing "+xmlfile+" ...")
                        os.remove(xmlfile)

            before = after