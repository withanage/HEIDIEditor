#!/usr/bin/python

import sys
import json
import optparse
from xml2json import xml2json


def run(infile, outfile):
    xmldata = open(infile).read()
    options = optparse.Values({'pretty': False})
    jsondata = xml2json(xmldata, options, 1)
    jsondata = "[" + jsondata + "]"
    # print jsondata


    with open(outfile, 'wb') as f:
        json.dump(jsondata, f, sort_keys=False, indent=4)


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    run(infile, outfile)