"""
A simple Python script to send messages to a sever over Bluetooth using
Python sockets (with Python 3.3 or above).
"""

import socket

serverMACAddress = '00:13:43:5B:93:92'
port = 5
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    #print(text)
    if text == "quit":
        s.send(bytes('$ 0 0\n','UTF -8'))
        break
    #print(bytes(text+'\n', 'UTF-8'))
    s.send(bytes(text+'\n', 'UTF-8'))
s.close()
