#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "withanage"
__date__ = "$Jun 25, 2012 2:43:33 PM$"

#import urllib
import pycurl
import cStringIO

class Storage:
    def __init__(self):
        #self.contents = ''
        self.contents = list()
        #self.line = 0

    def store(self, buf):
        #self.line = self.line + 1
        #self.contents = "%s%i: %s" % (self.contents, self.line, buf)
        self.contents.append(buf)

    def __str__(self):
        return self.contents



def oxgrarage_conversion(file_name):
    file_path = '/home/www-data/web2py/applications/mpt/uploads/'
    error_list = []
    retrieved_headers = Storage()
    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.WRITEFUNCTION, buf.write)
    #c.setopt(c.URL, "http://kjc-ws2:8080/ege-webservice//Conversions/docx%3Aapplication%3Avnd.openxmlformats-officedocument.wordprocessingml.document/TEI%3Atext%3Axml/conversion?properties=%3Cconversions%3E%3Cconversion%20index=%220%22%3E%3Cproperty%20id=%22oxgarage.getImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.getOnlineImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.lang%22%3Een%3C/property%3E%3Cproperty%20id=%22oxgarage.textOnly%22%3Efalse%3C/property%3E%3Cproperty%20id=%22pl.psnc.dl.ege.tei.profileNames%22%3Edefault%3C/property%3E%3C/conversion%3E%3C/conversions%3E")
    #c.setopt(c.URL, "http://kjc-ws2:8080/ege-webservice//Conversions/docx%3Aapplication%3Avnd.openxmlformats-officedocument.wordprocessingml.document/TEI%3Atext%3Axml/fo%3Aapplication%3Axslfo%2Bxml/conversion?properties=%3Cconversions%3E%3Cconversion%20index=%220%22%3E%3Cproperty%20id=%22oxgarage.getImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.getOnlineImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.lang%22%3Een%3C/property%3E%3Cproperty%20id=%22oxgarage.textOnly%22%3Efalse%3C/property%3E%3Cproperty%20id=%22pl.psnc.dl.ege.tei.profileNames%22%3Edefault%3C/property%3E%3C/conversion%3E%3Cconversion%20index=%221%22%3E%3Cproperty%20id=%22oxgarage.getImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.getOnlineImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.lang%22%3Een%3C/property%3E%3Cproperty%20id=%22oxgarage.textOnly%22%3Efalse%3C/property%3E%3Cproperty%20id=%22pl.psnc.dl.ege.tei.profileNames%22%3Edefault%3C/property%3E%3C/conversion%3E%3C/conversions%3E")
    #c.setopt(c.URL, "http://kjc-ws2.kjc.uni-heidelberg.de:8080/ege-webservice//Conversions/TEI%3Atext%3Axml/fo%3Aapplication%3Axslfo%2Bxml/conversion?properties=%3Cconversions%3E%3Cconversion%20index=%220%22%3E%3Cproperty%20id=%22oxgarage.getImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.getOnlineImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.lang%22%3Een%3C/property%3E%3Cproperty%20id=%22oxgarage.textOnly%22%3Efalse%3C/property%3E%3Cproperty%20id=%22pl.psnc.dl.ege.tei.profileNames%22%3Edefault%3C/property%3E%3C/conversion%3E%3C/conversions%3E")
    
    c.setopt(c.URL, "http://kjc-ws2.kjc.uni-heidelberg.de:8080/ege-webservice//Conversions/doc%3Aapplication%3Amsword/odt%3Aapplication%3Avnd.oasis.opendocument.text/TEI%3Atext%3Axml/conversion?properties=%3Cconversions%3E%3Cconversion%20index=%220%22%3E%3C/conversion%3E%3Cconversion%20index=%221%22%3E%3Cproperty%20id=%22oxgarage.getImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.getOnlineImages%22%3Etrue%3C/property%3E%3Cproperty%20id=%22oxgarage.lang%22%3Een%3C/property%3E%3Cproperty%20id=%22oxgarage.textOnly%22%3Efalse%3C/property%3E%3Cproperty%20id=%22pl.psnc.dl.ege.tei.profileNames%22%3Edefault%3C/property%3E%3C/conversion%3E%3C/conversions%3E")
    c.setopt(c.HTTPPOST, [("file", (c.FORM_FILE, file_path+file_name))])
    #c.setopt(c.VERBOSE, 1)
    c.setopt(c.HEADERFUNCTION, retrieved_headers.store)
    #c.setopt(c.WRITEFUNCTION, retrieved_headers.store)
    c.perform()
    c.close()
    i  = 0
    f = None
    rec_file_name = ''
    for  content in retrieved_headers.contents:
    	if 'filename' in content:
    		rec_file_name= str(content.split('filename=')[1].rsplit('"')[1])
        else:
    		 error_list.append('File '+file_name + 'not converted'   )

        try:
          f = open(rec_file_name, "w")
          f.write(buf.getvalue())
        except IOError:
          error.append(IOError)
        finally:
          f.close()
          buf.close()

    return error_list

if __name__ == "__main__":
    main()
