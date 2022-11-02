import serial
import numpy as np
import sys
import time
import csv

class serial_logger:

    def __init__(self):
        self.ser = serial.Serial(port = '/dev/ttyUSB0',
                    baudrate = 115200,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout = 0.5)
        
        if self.ser.is_open==True:
            print("\nSerial open. Configuration:\n")
            print(self.ser, "\n") #print serial parameters
        else:
            print("\n Serial open failed.\n")

        #TODO: read from file
        self.dict = {
            'Device Type': 0,
            'Time': 1,
            'Bicep': 2,
            'Tricep': 3,
            'Mode': 4,
            'Configured duel mode': 5,
            'Bicep Effort':6,
            'Tricep Effort': 7,
            'Tricep Dual Mode Effort Threshold': 8,
            'Biceps Dual Mode Effort Threshold': 9,
            'Bicep Sensor Gain': 10,
            'Tricep Sensor Gain': 11,
            'Bicep Movement Threshold': 12,
            'Tricep Movement Threshold': 13,
            'Joint Position': 14,
            'Battery Current': 15
        }

    #TODO: have connecting to serial from a file


    def start_log(self):
        Elbow_name = "./Elbow"+time.strftime("%m%d%Y-%H%M%S")+".csv"
        Hand_name = "./Hand"+time.strftime("%m%d%Y-%H%M%S")+".csv"
        while True:
            try:
                line = self.ser.readline().decode("utf-8")
                line_as_list = line.split(',')
                with open (Elbow_name, 'a') as f1, open (Hand_name, 'a') as f2:
                    writer_e = csv.writer(f1,quoting=csv.QUOTE_ALL,escapechar = '\n')
                    writer_h = csv.writer(f2,quoting=csv.QUOTE_ALL,escapechar = '\n')
                    if line_as_list[0] == '\x00E':
                        writer_e.writerow(line_as_list)
                    else:
                        writer_h.writerow(line_as_list)

            except KeyboardInterrupt:
                print('\nlog finished\n')
                break



    def tear_down(self):
        self.ser.close()

def main():
    logger = serial_logger()
    logger.start_log()
    logger.tear_down()

if __name__ == '__main__':
    main()