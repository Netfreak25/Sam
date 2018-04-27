#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import SocketServer
import sys
import cgitb; cgitb.enable()  ## This line enables CGI error reporting


class ThreadingCGIServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass


### Konfiguration laden / do not change
configfile = "./config.ini"
f = open(configfile, 'r')
configdb = {}

def getconfig(a):
    if len(configdb) == 0:
        for i in f:
            if i[0] != "#":
                x = i[:-1]
                y = x.split()
                if len(y) > 0:
                    configdb[y[0]] = y[2]
        return configdb[a]
    else:
        return configdb[a]

try:
    web_gui_port = int(getconfig('web_gui_port'))
except:
    web_gui_port = 8000
    
try:
    web_gui_ip = str(getconfig('web_gui_ip'))
    text_ip = str(web_gui_ip)
except:
    web_gui_ip = ""
    text_ip = "0.0.0.0"



#server = BaseHTTPServer.HTTPServer

handler = CGIHTTPServer.CGIHTTPRequestHandler
handler.cgi_directories = ["/htbin"]

print "The Admin Interface is running under:"
print "http://"+text_ip+":"+str(web_gui_port)+"/"

server = ThreadingCGIServer((web_gui_ip, web_gui_port), handler)
try:
    while 1:
        sys.stdout.flush()
        server.handle_request()
except KeyboardInterrupt:
    print "Gui stopped!"