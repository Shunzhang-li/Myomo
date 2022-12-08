import socket
import serial
import numpy as np
import sys
import time
import csv


class dynamic_threshold_controller:

    def __init__(self):
        self.serverMACAddress = '00:13:43:5B:93:92'
        self.port = 5
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.socket.connect((self.serverMACAddress,self.port))
        self.t_s = 0.1
        self.size = 1024
        self.init_tri_th = 10
        self.init_bi_th = 10
        self.socket.send(bytes('$ o ' + str(self.init_bi_th)+'\n', 'UTF-8'))
        self.socket.send(bytes('$ p '+str(self.init_tri_th)+'\n', 'UTF-8'))
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
        while True:
            try:
                last_time = init_time
                self.socket.send(bytes('$ b\n','UTF-8'))
                data = self.socket.recv(self.size)

                if data:
                    c_time = time.time()
                    data = data.decode("utf-8")
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
                
                    new_tri_th = self.init_tri_th - E_th
                    new_bi_th = self.init_bi_th + E_th
                    bi_msg = "$ o " + str(new_bi_th) 
                    tri_msg = "$ p " + str(new_tri_th) 
                    self.socket.send(bytes(bi_msg+'\n', 'UTF-8'))
                    self.socket.send(bytes(tri_msg+'\n', 'UTF-8'))
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