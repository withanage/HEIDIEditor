#!/usr/bin/python

import sys
import json
import optparse
import xmltodict


def run(infile, outfile):
    xmldata = open(infile).read()
    jsondata = xmltodict.parse(xmldata)
    with open(outfile, 'w+') as f:
        json.dump(jsondata, f, sort_keys=False, indent=4)


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    run(infile, outfile)