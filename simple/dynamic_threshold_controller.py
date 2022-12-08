import socket
import serial
import numpy as np
import sys
import time
import csv
import os

class dynamic_threshold_controller:

    def __init__(self):
        self.ser = serial.Serial(port = '/dev/ttyUSB0',
                    baudrate = 115200,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout = 0.5)
        self.serverMACAddress = '00:13:43:5B:93:92'
        self.port = 5
        self.socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.socket.connect((self.serverMACAddress,self.port))
        self.socket.send(bytes('$ o 10\n', 'UTF-8'))
        self.socket.send(bytes('$ p 10\n', 'UTF-8'))
        if self.ser.is_open==True:
            print("\nSerial open. Configuration:\n")
            print(self.ser, "\n") #print serial parameters
        else:
            print("\n Serial open failed.\n")

        self.dict = {
            'Device Type': 0,
            'Time': 1,
            'Tricep': 2,
            'Bicep': 3,
            'Mode': 4,
            'Configured duel mode': 5,
            'Tricep Effort':6,
            'Bicep Effort': 7,
            'Tricep Dual Mode Effort Threshold': 8,
            'Bicep Dual Mode Effort Threshold': 9,
            'Bicep Sensor Gain': 10,
            'Tricep Sensor Gain': 11,
            'Bicep Movement Threshold': 12,
            'Tricep Movement Threshold': 13,
            'Joint Position': 14,
            'Battery Current': 15
        }

        self.polymodel = [1, 0]

    def change_polymodel(self,p_model):
        self.polymodel = p_model

    def tear_down(self):
        self.ser.close()
        self.socket.close()

    def start_controller(self):
        i_JA = self.dict["Joint Position"]
        i_tri_th = self.dict["Tricep Dual Mode Effort Threshold"]
        i_Bi_th = self.dict["Bicep Dual Mode Effort Threshold"]
        init_time = time.time()
        Elbow_name = "./Elbow"+time.strftime("%m%d%Y-%H%M%S")+".csv"

        #init_tri_th = line_as_list[i_tri_th]
        #init_bi_th = line_as_list[i_Bi_th]
        init_tri_th = -21
        init_bi_th = -21
        JA = -21
        fileout = []
        while True:
            try:
                #TODO Update only a few 0.1 s
                #os.system('clear')
                line = self.ser.readline().decode("utf-8")
                line_as_list = line.split(',')
                print("line: "+str(line))

                if line_as_list[0] != '\x00E':
                    continue
                if init_bi_th < -20 and init_tri_th < -20:
                    init_tri_th = int(line_as_list[i_tri_th])
                    init_bi_th = int(line_as_list[i_Bi_th])
                
                JA = float(line_as_list[i_JA])*np.pi/180
                print("JA: "+str(JA*180/np.pi))
                E_th = int(np.polyval(self.polymodel,JA))
                print("Bi: "+line_as_list[i_Bi_th] +" Tri: "+ line_as_list[i_tri_th])
                new_tri_th = init_tri_th - E_th
                new_bi_th = init_bi_th + E_th
                #print("before send JA: "+line_as_list[i_JA]+" new Bi "+str(new_bi_th)+" new Tri "+str(new_tri_th))
                bi_msg = "$ o " + str(new_bi_th) 
                tri_msg = "$ p " + str(new_tri_th) 
                #self.socket.send(bytes(bi_msg+'\n', 'UTF-8'))
                #self.socket.send(bytes(tri_msg+'\n', 'UTF-8'))
                c_time = time.time() - init_time
                line_as_list.append(c_time)
                fileout.append(line_as_list)
                #with open (Elbow_name, 'a') as f1:
                #    writer_e = csv.writer(f1,quoting=csv.QUOTE_ALL,escapechar = '\n')
                #    writer_e.writerow(line_as_list)
                #f1.close()
                #print("new it JA: "+str(JA*180/np.pi)+" new Bi "+str(new_bi_th)+" new Tri "+str(new_tri_th))
                #time.sleep(0.5)

            except KeyboardInterrupt:
                with open (Elbow_name, 'a') as f1:
                    for line in fileout:
                        writer_e = csv.writer(f1,quoting=csv.QUOTE_ALL,escapechar = '\n')
                        writer_e.writerow(line)
                f1.close()
                self.socket.send(bytes('$ o 10\n', 'UTF-8'))
                self.socket.send(bytes('$ p 10\n', 'UTF-8'))
                print('\nlog finished\n')
                break


def main(p = [0,0]):
    p = [float(x) for x in p] 
    controller = dynamic_threshold_controller()
    controller.change_polymodel(p)
    controller.start_controller()
    controller.tear_down()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        p = sys.argv[1:]
        main(p)
    else:
        main()