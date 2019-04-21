import websocket
import time
import logging
import threading

passwd="123456"

class littlesock():
    messages=[]
    def __init__(self,sock,logger:logging.getLogger=logging):
        self.logger=logger
        websocket.enableTrace(True)
        self.web = websocket.WebSocketApp(sock, on_message=self.OnMess, on_error=self.OnError)
        self.T=threading.Thread(target=self.web.run_forever)
        self.T.daemon = True
        # self.web.keep_running = 1
        self.T.start()
        conn_timeout = 5
        try:
            while not self.web.sock.connected and conn_timeout:
                time.sleep(1)
                conn_timeout -= 1
        except AttributeError:
            self.messages.append("failed")
    def __enter__(self):
        return self

    def OnMess(self,ws,message=""):
        if not message:message=ws
        logging.info(message)
        if len(self.messages)>10:self.messages.pop(0)
        self.messages.append(message)

    def OnError(self,ws,error=""):
        logging.warning(error)

    def __exit__(self, exc_type="", exc_val="", exc_tb=""):
        self.web.close()
        #可以不用↓
        self.T.join()
        self.logger.info(exc_type)
        self.logger.info(exc_val)
        self.logger.info(exc_tb)
        print("messg::",self.messages,end=" ")
        return self.messages

import re,socket
class espweber():
    def __init__(self,place,normal=0,logger=logging):
        self.normal=normal
        try:place=int(place)
        except:
            if not re.search("\.",place):place+=".mshome.net"

            print(place)
            try:place=socket.gethostbyname(place)
            except:place=socket.gethostbyname("ESP_"+place)
        if type(place)==int:
            place=str(place)
            place="ws://192.168.1." + place + ":8266/"
        else:
            place="ws://"+place+":8266/"

        logger.debug(place)
        self.WS = littlesock(place,logger)

        while not len(self.WS.messages):time.sleep(0)
        self.saylines(passwd)

        if not self.normal:"\x01"

    def didline(self):
        if self.normal:
            return b"\r\n"
        return b"\x04"
    def saylines(self,p):
        print("saylines"+str(p))
        if not re.search("\r\n",p) and re.search("\n",p):
            print("DiDi")
            p=re.split("\n",p)
        if type(p)==list:
            for k in p:self.saylines(k)
        else:
            if type(p)==str:p=bytes(p,"utf-8")
            self.WS.web.send(p+self.didline())
    def start(self):
        self.saylines("start()")

    def turnoff(self,restart=0):
        if restart: self.saylines("from machine import *;reset()")
        # if restart: self.saylines("from sys import *;exit()")
        self.WS.__exit__()


#fake
class espweber1():
    def __init__(self,*args):
        print(*args)
        time.sleep(5)
    def saylines(self,s):
        print("said "+s)
    def turnoff(self):
        pass
    def start(self):
        pass

def Pincontroller():
    C.saylines("from machine import Pin;P=Pin(0,Pin.OUT)")
    while 1:
        n = input()
        if n == "1" or n == "0":
            print("said {}".format(n))
            C.saylines("P.value({})".format(n))
        else:
            break
# import sys
# print(sys.argv)




if __name__ == '__main__':
    Log = logging.getLogger()
    Log.setLevel(logging.DEBUG)
    if(1):
        # C=espweber(185)
        # C=espweber(113)
        # C=espweber("ESP_4C3FA7",1,Log)
        C=espweber("ESP_CB0055",1,Log)
        # C=espweber(142,1,Log)
        # C=espweber("192.168.1.50",1,Log)
        # C.saylines("D7.value(0)")
        # C=espweber(98,1)
        while 1:
            C.saylines(input())
            if "" != input():
                C.turnoff()
                break
        # time.sleep(1)
        C.turnoff()
