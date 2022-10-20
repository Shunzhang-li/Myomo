import socket
import time
serverMACAddress = '00:13:43:5B:93:92'
port = 5
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
for i in range(5):
    text = '$ 0 ' + str(i%4)
    print('command: '+ text)
    s.send(bytes(text+'\n', 'UTF-8'))
    time.sleep(1)

s.close()
