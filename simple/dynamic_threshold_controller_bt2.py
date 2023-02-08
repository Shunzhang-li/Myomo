import socket
import serial
import numpy as np
import sys
import time
import csv
import random


class dynamic_threshold_controller:

    def __init__(self):
        self.serverMACAddress = '00:13:43:5B:93:92'
        self.port = 5
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.socket.connect((self.serverMACAddress,self.port))
        self.t_s = 0.3
        self.size = 256
        self.init_tri_th = 20
        self.init_bi_th = 20
        #self.socket.send(bytes('$ o ' + str(self.init_bi_th)+'\n', 'UTF-8'))
        #self.socket.send(bytes('$ p '+str(self.init_tri_th)+'\n', 'UTF-8'))
        self.polymodel = [1, 0]

    def change_polymodel(self,p_model):
        self.polymodel = p_model

    def tear_down(self):
        #self.ser.close()
        self.socket.close()

    def start_controller(self):
        print("\ncontroller start\n")
        init_time = time.time()
        input_name = "./Input"+time.strftime("%m%d%Y-%H%M%S")+".csv"

        JA = -21
        fileout = []
        self.socket.send(bytes('$\x1bz\n','UTF-8'))
        time.sleep(0.1)
        predata = self.socket.recv(self.size)
        predata = predata.decode("utf-8")
        predata = predata.replace("\n"," ").split(" ")
        dmode_p = predata[6:22]
        print(dmode_p)
        while True:
            try:
                #TODO read system state using s.send(bytes('$\x1bz\n','UTF-8')), write to use $\x1by only once?
                last_time = init_time
                """
                self.socket.send(bytes('$\x1bz\n','UTF-8'))
                time.sleep(0.05)
                data2 = self.socket.recv(self.size)

                if data2:
                    data2 = data2.decode("utf-8")
                    print("data2: "+data2)

                """    

                self.socket.send(bytes('$ b\n','UTF-8'))
                #time.sleep(1)
                data = self.socket.recv(self.size)

                if data:
                    #TODO read threshold and other system state from the command
                    c_time = time.time()
                    data = data.decode("utf-8")
                    #print("data: "+data)
                    if(data[0] != '$'):
                        ct = time.time() - init_time
                        if self.t_s - ct > 0:
                            time.sleep(self.t_s - ct)
                        continue
                    getme = data.split('\n')
                    getme = getme[0].split(' ')
                    if (len(getme) < 3):
                        ct = time.time() - init_time
                        if self.t_s - ct > 0:
                            time.sleep(self.t_s - ct)
                        continue
                    JA = getme[2]
                    print("JA: "+JA)
                    JA_rad = int(JA)*np.pi/180
                    E_th = int(np.polyval(self.polymodel,JA_rad))
                
                    new_tri_th = self.init_tri_th - E_th + random.randrange(5)
                    new_bi_th = self.init_bi_th + E_th + random.randrange(5)

                    #TODO update message sent
                    msg_lst = dmode_p[1:] 
                    msg_lst[3] = str(new_bi_th)
                    msg_lst[4] = str(new_tri_th)
                    msg = " " 
                    for m in msg_lst:
                        msg = msg + m +" "
                    
                    new_msg = "$\x1by" + msg 
                    print("nm: "+new_msg)
                    #tri_msg = "$ p " + str(new_tri_th) 
                    #self.socket.send(bytes(bi_msg+'\n', 'UTF-8'))
                    self.socket.send(bytes(new_msg+' 1\n', 'UTF-8'))
                    c_time = time.time()
                    
                    line_as_list = [JA,new_bi_th,new_tri_th,c_time]
                    fileout.append(line_as_list)
                    ct = time.time() - init_time
                    if self.t_s - ct > 0:
                        time.sleep(self.t_s - ct)


            except KeyboardInterrupt:
                print("\ncontroller finished, start logging\n")
                with open (input_name, 'a') as f1:
                    for line in fileout:
                        
                        writer_e = csv.writer(f1,quoting=csv.QUOTE_ALL,escapechar = '\n')
                        writer_e.writerow(line)
                f1.close()
                self.socket.send(bytes('$ o 10\n', 'UTF-8'))
                self.socket.send(bytes('$ p 10\n', 'UTF-8'))
                print('\nlog finished\n')
                self.tear_down()
                break


def main(p = [0,0]):
    p = [float(x) for x in p] 
    controller = dynamic_threshold_controller()
    controller.change_polymodel(p)
    controller.start_controller()


if __name__ == '__main__':
    if len(sys.argv) > 2:
        p = sys.argv[1:]
        main(p)
    else:
        main()