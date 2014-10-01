#!/usr/bin/python
# -*- coding: utf-8 -*-



import cgitb
import logging
import os
import stat
import time
from datetime import datetime
import sys
from xml2json import xml2json
import optparse
import json
import shutil

sys.path.append('../meTypeset/bin')
import meTypeset


cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='typeset.log')


#### Constant variables ####
TMP_DIR = '../html/files'
UPLOAD_DIR = '../html/uploads'
METADATA_PATH = os.path.abspath('../meTypeset/metadata/metadataSample.xml')
PERM_666 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)


def typeset(item):
    bookname = item.split('_',1)
    logging.info("\t"+str(datetime.now().time())+":\t\t Checking validation "+item+" ...")
    if not os.path.isfile(TMP_DIR+"/"+item):
        logging.debug("\t"+str(datetime.now().time())+":\t\t Path error: "+item)
        return
    filename = os.path.splitext(bookname[1])
    if len(filename) != 2:
        logging.debug("\t"+str(datetime.now().time())+":\t\t Filename error: "+item)
        return
    if not filename[1] in ['.doc', '.docx', '.odt']:
        logging.debug("\t"+str(datetime.now().time())+":\t\t Filetype error: "+item)
        return

    bookname_dir = UPLOAD_DIR+"/"+bookname[0]
    out_dir = bookname_dir+"/"+"out_"+filename[0]
    if os.path.exists(out_dir):
        logging.debug("\t"+str(datetime.now().time())+":\t\t "+out_dir+" already exists. remove it.")
        shutil.rmtree(out_dir)
    opt = filename[1].strip('.') + " " + bookname_dir + "/" + bookname[1]  + " " + out_dir + " -m " + METADATA_PATH
    logging.info("\t"+str(datetime.now().time())+":\t\t [-------meTypeset-------]")
    logging.info("\t"+str(datetime.now().time())+":\t\t meTypeset.py "+opt)
    log = meTypeset.test(opt)
    logging.info("\t"+str(datetime.now().time())+":\t\t meTypeset debug log: \n"+log)
    
    logging.info("\t"+str(datetime.now().time())+":\t\t Generating JSON ...")
    nlmfile = out_dir+"/"+"nlm"+"/"+"out.xml"
    xmldata = open(nlmfile).read()
    options = optparse.Values({'pretty': True})
    jsondata = xml2json(xmldata, options, 1)
    # logging.info("\t"+str(datetime.now().time())+":\t\t JSON data: \n"+jsondata)

    if not os.path.isdir(bookname_dir+"/"+"json"):
        logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+bookname_dir+"/"+"json"+" ...")
        os.mkdir(bookname_dir+"/"+"json", 0775)
    jsonfile = bookname_dir+"/"+"json"+"/"+filename[0]+".json"
    if os.path.exists(jsonfile):
        logging.debug("\t"+str(datetime.now().time())+":\t\t "+jsonfile+" already exists. remove it.")
        os.remove(jsonfile)
    logging.info("\t"+str(datetime.now().time())+":\t\t Writing JSON to "+jsonfile+" ...")
    with open(jsonfile, 'w+') as f:
        json.dump("["+jsondata+"]", f, sort_keys=False, indent=4)

    if not os.path.isdir(bookname_dir+"/"+"xml"):
        logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+bookname_dir+"/"+"xml"+" ...")
        os.mkdir(bookname_dir+"/"+"xml", 0775)
    xmlfile = bookname_dir+"/"+"xml"+"/"+filename[0]+".xml"
    if os.path.exists(xmlfile):
        logging.debug("\t"+str(datetime.now().time())+":\t\t "+xmlfile+" already exists. remove it.")
        os.remove(xmlfile)
    logging.info("\t"+str(datetime.now().time())+":\t\t Copying XML to "+xmlfile+" ...")
    shutil.copyfile(nlmfile, xmlfile)


def main():
    logging.info("\n\t================main() in typeset2.py "+str(datetime.now())+"=================\n")

    for item in os.listdir(TMP_DIR):
        logging.info("\t"+str(datetime.now().time())+":\t Processing "+item+" ...")
        if(os.path.isfile(TMP_DIR+"/"+item)):
            # Check Bookname
            bookname = item.split('_',1)
            bookname_dir = UPLOAD_DIR+"/"+bookname[0]
            # Make Directory
            if not os.path.isdir(bookname_dir):
                logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+bookname_dir+"/ ...")
                os.mkdir(bookname_dir, 0775)
            # Copy File
            filename = os.path.splitext(bookname[1])
            if(filename[1] in ['.doc', '.docx', '.odt']):
                logging.info("\t"+str(datetime.now().time())+":\t\t Copying file to "+bookname_dir+"/"+bookname[1]+" ...")
                shutil.copy2(TMP_DIR+"/"+item, bookname_dir+"/"+bookname[1])
            else:
                media_dir = bookname_dir+"/media"
                if not os.path.exists(media_dir):
                    logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+media_dir+"/ ...")
                    os.mkdir(media_dir, 0775)
                logging.info("\t"+str(datetime.now().time())+":\t\t Copying file to "+media_dir+"/"+bookname[1]+" ...")
                shutil.copy2(TMP_DIR+"/"+item, media_dir+"/"+bookname[1])
            # Call meTypeset
            typeset(item)
        logging.info("\t"+str(datetime.now().time())+":\t Done." )



if __name__ == "__main__":
    main()


    # jump to next page
    print "Content-Type: text/html"
    print "Location: http://"+os.environ['HTTP_HOST']+"/HEIDIEditor/html/step2.html\n"