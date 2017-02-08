#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""
trafficGenerator is a small program used to simulate HTTPS and HTTP conections between a client and a web server.
"""

import http.client
import urllib.parse
import time

dest = ""
url = ""
login = ""
pwd = ""

def readConf():

    global dest
    global url
    global login
    global pwd

    file = open("conf.txt", "r")
    conf = file.read().split("\n")
    
    dest = conf[0]
    url = conf[1]
    login = conf[2]
    pwd = conf[3]

    print(conf)
    file.close()


def httpsConnection():

    errCMP = 0

    while 1 :
    
        try:

            parameters = urllib.parse.urlencode({"username": login, "password": pwd})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "texe/html"}
            connection = http.client.HTTPSConnection(dest, timeout=4)
            connection.request("POST", url, parameters, headers)
            response = connection.getresponse()
            response.read()
            print(response.status, response.reason)
            connection.close()
            time.sleep(5)
            
        except:
            
            print("Error HTTPS Connection")
            errCMP += 1
            time.sleep(3)
            
            if errCMP >= 3:
                break

def httpConnection():

    errCMP = 0

    while 1 :
    
        try:

            parameters = urllib.parse.urlencode({"username": login, "password": pwd})
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "texe/html"}
            connection = http.client.HTTPConnection(dest, timeout=4)
            connection.request("POST", url, parameters, headers)
            response = connection.getresponse()
            response.read()
            print(response.status, response.reason)
            connection.close()
            time.sleep(5)
            
        except:
            
            print("Error HTTP Connection")
            errCMP += 1
            time.sleep(3)
            
            if errCMP >= 3:
                break
            

if __name__ == "__main__":

    readConf()

    while 1:
        
        print("*** Trying HTTPS Connection ***")
            
        httpsConnection()

        print("*** Switching to HTTP Connection ***")

        httpConnection()
            

            
