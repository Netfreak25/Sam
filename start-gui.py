#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting



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
except:
    web_gui_ip = ""

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = (web_gui_ip, web_gui_port)
handler.cgi_directories = ["/htbin"]

httpd = server(server_address, handler)
httpd.serve_forever()