#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
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
    text_ip = str(web_gui_ip)
except:
    web_gui_ip = ""
    text_ip = "0.0.0.0"


class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        print(self.headers)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")
        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        
        print(request_headers)
        print(self.rfile.read(length))
        print("<----- Request End -----\n")
        
        self.send_response(200)


#server = BaseHTTPServer.HTTPServer
server = HTTPServer(('', web_gui_port), RequestHandler)
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = (web_gui_ip, web_gui_port)
handler.cgi_directories = ["/htbin"]

print "The Admin Interface is running under:"
print "http://"+text_ip+":"+str(web_gui_port)+"/"
httpd = server(server_address, handler)
httpd.serve_forever()