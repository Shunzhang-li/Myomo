
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
#s.listen(backlog)
try:
#    client, address = s.accept()
    while c > -1:
        c =c + 1
        init_time = time.time()
        #print("interval: " + str(init_time - last_time))
        last_time = init_time
        s.send(bytes('$ y\n','UTF-8'))
        data = s.recv(size)
        if data:
            c_time = time.time()
            data = data.decode("utf-8")
            #print("len: " + str(len(data)))
            print("data: "+data)
            if(data[0] != '$'):
                ct = time.time() - init_time
                if ts - ct > 0:
                    time.sleep(ts - ct)
                continue
            m = c%55+9
            s.send(bytes('$ o '+ str(1+m)+'\n','UTF-8'))    
            s.send(bytes('$ p '+str(1+m)+'\n','UTF-8'))
            getme = data.split('\n')
            getme = getme[0].split(' ')
            if (len(getme) < 3):
                ct = time.time() - init_time
                if ts - ct > 0:
                    time.sleep(ts - ct)
                continue
        #s.send(bytes('$ y\n','UTF-8'))
        #data2 = s.recv(size)
        #if data2:
        #    c_time = time.time()
        #    data2 = data2.decode("utf-8")
            #print("len: " + str(len(data)))
        #    print("data2: "+data2)
            #if(data2[0] != '$'):
            #    ct = time.time() - init_time
            #    if ts - ct > 0:
            #        time.sleep(ts - ct)
            #    continue
            #getme = data.split('\n')
            #getme = getme[0].split(' ')
            #if (len(getme) < 3):
            #    ct = time.time() - init_time
            #    if ts - ct > 0:
            #        time.sleep(ts - ct)
            #    continue
        #print(str(c_time)+ " "+ getme[2])
        ct = time.time() - init_time
        if ts - ct > 0:
            time.sleep(ts - ct)
        
except:
#    client.close()
    #print(e)
    s.close()