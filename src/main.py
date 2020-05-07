#import BaseHTTPServer, SimpleHTTPServer
#import ssl

#httpd = BaseHTTPServer.HTTPServer(('localhost', 8081), SimpleHTTPServer.SimpleHTTPRequestHandler)

#httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=)


import http.server
import socketserver

port = 8081
handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", port), handler) as httpd:
    httpd.serve_forever()