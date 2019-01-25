#  coding: utf-8 
import socketserver
import re
import mimetypes
import os
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#reference: split by space : https://blog.csdn.net/hawkerou/article/details/53518154
#           https://stackoverflow.com/questions/4690600/python-exception-message-capturing

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))
        data = self.data.decode()
        #split the data by space 
        data_list = re.split(r' ',data)
        #print ("data_list : ", data_list)

        request_method = data_list[0]

        if request_method == "GET":
            ori_path = data_list[1]
            path = 'www' + ori_path
            #print(path)
            #ignore the favicon request
            if path == "www/favicon.ico":
                return

            try:
                file = open(path).read()
                file2 = open(path)
                content_type = mimetypes.guess_type(path)
                #print("content_type:", content_type[0])
                real_path = os.path.abspath(file2.name)
                relative_path = os.getcwd()+"/www"
                #print("relative_path:",relative_path)
                #print("realpath:", real_path)

                #check if the file is out of the "www" file
                if relative_path in real_path:
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                    if content_type[0] != None:
                        self.request.sendall(bytearray("Content-Type:" + content_type[0] + "\r\n",'utf-8'))
                    self.request.sendall(bytearray("Connection: keep-alive\r\n\r\n",'utf-8'))
                    self.request.sendall(bytearray(file,'utf-8'))
                else:
                    self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                    self.request.sendall(bytearray("Connection: closed\r\n\r\n",'utf-8')) 



            except IsADirectoryError as e:
                #print("last char:", path[-1])
                if path[-1] == '/':
                    path = path + "index.html"
                    file = open(path).read()
                    file2 = open(path)
                    content_type = mimetypes.guess_type(path)
                    real_path = os.path.abspath(file2.name)
                    relative_path = os.getcwd()+"/www"
                    #print("content_type:", content_type[0])
                    if relative_path in real_path:

                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
                        if content_type[0] != None:
                            self.request.sendall(bytearray("Content-Type:" + content_type[0] + "\r\n",'utf-8'))
                        self.request.sendall(bytearray("Connection: keep-alive\r\n\r\n",'utf-8'))
                        self.request.sendall(bytearray(file,'utf-8'))
                    else:
                        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                        self.request.sendall(bytearray("Connection: closed\r\n\r\n",'utf-8')) 


                else:
                    print("301 move per...")
                    #print("e is :", str(e))
                    #print("type of e:",type(e))
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))
                    new_path = ori_path + "/"
                    self.request.sendall(bytearray("Location:" + new_path + "\r\n",'utf-8'))
                    self.request.sendall(bytearray("text/html\r\n",'utf-8'))
                    self.request.sendall(bytearray("Connection: keep-alive\r\n\r\n",'utf-8'))
                    return

            except FileNotFoundError as e:
                #print("e is :", str(e))
                #print("type of e:",type(e))
                print("404 NOt found")
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                self.request.sendall(bytearray("text/html\r\n",'utf-8'))
                self.request.sendall(bytearray("Connection: closed\r\n\r\n",'utf-8'))                
                return

            except NotADirectoryError as e:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
                self.request.sendall(bytearray("text/html\r\n",'utf-8'))
                self.request.sendall(bytearray("Connection: closed\r\n\r\n",'utf-8'))
                
            #finally:
                #self.sendback("HTTP/1.1 200 OK\r\n", "text/html\r\n", "keep-alive\r\n", file)


        #if not get method
        else:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
            #self.request.sendall(bytearray("text/html\r\n",'utf-8'))
            self.request.sendall(bytearray("Connection: closed\r\n\r\n",'utf-8'))





if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()











    
