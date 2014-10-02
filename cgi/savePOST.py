#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import os
import sys
import codecs
import Cookie

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

cgitb.enable()

print "Content-type: text/html; charset=UTF-8"

#check method
if ( os.environ['REQUEST_METHOD'] != "POST" ):
    print "invalid method"
    sys.exit()

form = cgi.FieldStorage()
#check parameter
if not ( form.has_key("name") and form.has_key("comment") ):
    print "invalid parameters"
    sys.exit()

#write data
file = None
try:
    file = open("work/test.txt", "a")
    file.write(form["name"].value + "," + form["comment"].value + "\r\n")
    print "succeeded"
except IOError:
    print "failed"
finally:
    if(file):
        file.close()