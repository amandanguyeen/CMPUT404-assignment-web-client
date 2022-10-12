#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright 2022 Amanda Nguyen
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
from urllib.parse import urlparse, urlencode

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def parse_url(self, url):
        result = urlparse(url)
        if ':' in result.netloc:
            host, port = result.netloc.split(':')
        else:
            host = result.netloc
            port = 80

        if result.path == '':
            path = '/'
        else:
            path = result.path
            
        return host, int(port), path

    def parse_response(self, data):
        info, body = data.split("\r\n\r\n")
        split_data = info.split("\r\n")
        status_code = split_data[0].split(' ')[1]
        return int(status_code), body

    # Author: TRIANGLES, October 12, https://www.internalpointers.com/post/making-http-requests-sockets-python
    def GET(self, url, args=None):
        host, port, path = self.parse_url(url)
        self.connect(host, port)

        self.sendall(f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n")

        response = self.recvall(self.socket)
        print(response)
        status_code, body = self.parse_response(response)
        
        self.close()
        return HTTPResponse(status_code, body)

    # Author: sauerburger, October 12, https://stackoverflow.com/questions/45695168/send-raw-post-request-using-socket
    def POST(self, url, args=None):
        host, port, path = self.parse_url(url)
        self.connect(host, port)

        #Author: Alex R, October 12, https://stackoverflow.com/questions/54897849/circular-issue-attempt-to-send-form-url-encoded-data-causes-typeerror-cant-co
        if args != None:
            body = urlencode(args)
            self.sendall(f"POST {path} HTTP/1.1\r\nHost:{host}\r\nContent-Type: application/x-www-form-urlencoded\\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n{body}\r\n")
        else:
            self.sendall(f"POST {path} HTTP/1.1\r\nHost:{host}\r\nContent-Type: application/json\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        
        response = self.recvall(self.socket)
        print(response)
        status_code, body = self.parse_response(response)

        self.close()
        return HTTPResponse(status_code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
