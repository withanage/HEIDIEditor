#!/usr/bin/python

import SimpleHTTPServer
import SocketServer
import logging
import cgi, cgitb
import sys
from upload import save_file


cgitb.enable()
logging.basicConfig(level=logging.DEBUG, filename='HEIDIEditor/cgi/serverlog.txt')

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.debug("==========do_GET==========")
        logging.debug(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.debug("==========do_POST==========")
        logging.debug(self.headers)
        save_file('file', '../html/files')
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def run(port=8000):
    httpd = SocketServer.TCPServer(("", port), ServerHandler)
    print 'Serving HTTPServer on PORT', port, '...'
    httpd.serve_forever()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()
