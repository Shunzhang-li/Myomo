
import time
import socket


serverMACAddress = '00:13:43:5B:93:92'
port = 5
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
backlog = 1
size = 1024
c = 0
ts = 1
last_time = 0

try:
    while c > -1:
        c =c + 1
        print("c: "+str(c))
        init_time = time.time()
        #print("interval: " + str(init_time - last_time))
        last_time = init_time
        s.send(bytes('$\x1bz\n','UTF-8'))
        #s.send(bytes('\n','UTF-8'))
        
        data1 = s.recv(size)
        if data1:
            data1 = data1.decode("utf-8")
            print("data ez: "+data1)

        ct = time.time() - init_time
        if ts - ct > 0:
            time.sleep(ts - ct)

        s.send(bytes('$b\n','UTF-8'))
        data2 = s.recv(size)
        if data2:
            data2 = data2.decode("utf-8")
            print("data jp: "+data2)
        
        

        
except:
#    client.close()
    #print(e)
    s.close()