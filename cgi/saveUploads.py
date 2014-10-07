#!/usr/bin/python
# -*- coding: utf-8 -*-

# show progress bar
print 'Content-Type: text/html\n'
print '<html><head>'
print '<title>typesetting | HEIDIEditor</title>'
print '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">'
print '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>'
print '</head><body><div class="container">'
print '<h1 style="text-align:center; margin-top:150px">Typesetting...</h1>'
print '<div class="progress progress-striped active" style="width:50%; margin: 0 auto">'
print '<div class="progress-bar progress-bar-primary" style="width:100%"></div>'
print '</div></div></body></html>'



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

sys.path.append('../../meTypeset/bin')
import meTypeset


cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='typeset.log')


#### Constant variables ####
TMP_DIR = '../html/files'
UPLOAD_DIR = '../html/uploads'
METADATA_PATH = os.path.abspath('../../meTypeset/metadata/metadataSample.xml')
METADATA_NAME = 'metadata.xml'
PERM_666 = (stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
MEDIA_LIST = ['.jpg', '.jpeg', '.gif', '.tiff', '.esp', '.wav', '.mp3', '.mp4']
DOC_LIST = ['.doc', '.docx', '.odt']


def typeset(item):
    logging.info("\t"+str(datetime.now().time())+":\t\t Checking validation "+item+" ...")
    if not os.path.isfile(TMP_DIR+"/"+item):
        logging.debug("\t"+str(datetime.now().time())+":\t\t Path error: "+item)
        return
    bookname = item.split('_',1)
    if len(bookname) < 2:
        logging.debug("\t"+str(datetime.now().time())+":\t\t Filename error: "+item)
        return
    filename = os.path.splitext(bookname[1])
    if len(filename) != 2:
        logging.debug("\t"+str(datetime.now().time())+":\t\t Filename error: "+item)
        return


    bookname_dir = UPLOAD_DIR+"/"+bookname[0]
    out_dir = bookname_dir+"/"+"out_"+filename[0]
    if os.path.exists(out_dir):
        logging.debug("\t"+str(datetime.now().time())+":\t\t "+out_dir+" already exists. remove it.")
        shutil.rmtree(out_dir)
    opt = filename[1].strip('.') + " " + bookname_dir + "/" + bookname[1]  + " " + out_dir + " -d -m " + METADATA_PATH
    logging.info("\t"+str(datetime.now().time())+":\t\t [-------meTypeset-------]")
    logging.info("\t"+str(datetime.now().time())+":\t\t meTypeset.py "+opt)
    log = meTypeset.test(opt)
    logging.info("\t"+str(datetime.now().time())+":\t\t meTypeset debug log: \n"+log)

    nlmfile = out_dir+"/"+"nlm"+"/"+"out.xml"
    # logging.info("\t"+str(datetime.now().time())+":\t\t Generating JSON ...")
    # xmldata = open(nlmfile).read()
    # jsondata = xmltodict.parse(xmldata)
    # logging.info("\t"+str(datetime.now().time())+":\t\t JSON data: \n"+jsondata)

    # if not os.path.isdir(bookname_dir+"/"+"json"):
    # logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+bookname_dir+"/"+"json"+" ...")
    #    os.mkdir(bookname_dir+"/"+"json", 0775)
    # jsonfile = bookname_dir+"/"+"json"+"/"+filename[0]+".json"
    # if os.path.exists(jsonfile):
    #     logging.debug("\t"+str(datetime.now().time())+":\t\t "+jsonfile+" already exists. remove it.")
    #     os.remove(jsonfile)
    # logging.info("\t"+str(datetime.now().time())+":\t\t Writing JSON to "+jsonfile+" ...")
    # with open(jsonfile, 'w+') as f:
    #     json.dump(jsondata, f, sort_keys=False, indent=4)

    if not os.path.isdir(bookname_dir+"/"+"xml"):
        logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+bookname_dir+"/"+"xml"+" ...")
        os.mkdir(bookname_dir+"/"+"xml", 0775)
    xmlfile = bookname_dir+"/"+"xml"+"/"+filename[0]+".xml"
    if os.path.exists(xmlfile):
        logging.debug("\t"+str(datetime.now().time())+":\t\t "+xmlfile+" already exists. remove it.")
        os.remove(xmlfile)
    logging.info("\t"+str(datetime.now().time())+":\t\t Copying XML to "+xmlfile+" ...")
    shutil.copyfile(nlmfile, xmlfile)
    logging.info("\t"+str(datetime.now().time())+":\t\t Copying metadata file to "+bookname_dir+" ...")
    shutil.copyfile(METADATA_PATH, bookname_dir+"/"+METADATA_NAME)


def main():
    logging.info("\n\t================main() in saveUploads.py "+str(datetime.now())+"=================\n")

    # set METADATA_PATH
    files = os.listdir(TMP_DIR)
    if(METADATA_NAME in files):
        METADATA_PATH = os.path.abspath(TMP_DIR+"/"+METADATA_NAME)
        metafile = os.open(METADATA_PATH, os.O_RDONLY)
        os.fchmod(metafile, PERM_666)
        os.close(metafile)

    for item in files:
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
            if(filename[1].lower() in DOC_LIST):
                logging.info("\t"+str(datetime.now().time())+":\t\t Copying file to "+bookname_dir+"/"+bookname[1]+" ...")
                shutil.copy2(TMP_DIR+"/"+item, bookname_dir+"/"+bookname[1])

                # Call meTypeset
                typeset(item)

            elif(filename[1].lower() in MEDIA_LIST):
                media_dir = bookname_dir+"/media"
                if not os.path.exists(media_dir):
                    logging.info("\t"+str(datetime.now().time())+":\t\t Making directory "+media_dir+"/ ...")
                    os.mkdir(media_dir, 0775)
                logging.info("\t"+str(datetime.now().time())+":\t\t Copying file to "+media_dir+"/"+bookname[1]+" ...")
                shutil.copy2(TMP_DIR+"/"+item, media_dir+"/"+bookname[1])

        logging.info("\t"+str(datetime.now().time())+":\t Done." )



if __name__ == "__main__":
    main()

    # jump to next page
    #print 'Content-Type: text/html\n'
    print "Location: http://"+os.environ['HTTP_HOST']+"/HEIDIEditor/html/step2.html\n"