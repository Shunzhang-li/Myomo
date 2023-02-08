import socket
import serial
import numpy as np
import sys
import time
import csv

class auto_exp:

    def __init__(self):
        self.dict = {
            'Device Type': 0,
            'Time': 1,
            'Tricep': 2,
            'Bicep': 3,
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

    def data_fit(self, data):
        avg = data[:,0]
        angle = data[:,1]
        deg1 = np.polyfit(angle,avg,1)
        #deg2 = np.polyfit(angle,avg,2)
        return deg1

    def file_read(self, file):
        try:
            line_count = 0
            bit = 0
            trit = 0
            angt = 0
            with open(file, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for line in reader:
                    tri = int(line[2])
                    bi = int(line[3])
                    ang = int(line[-4])
                    line_count+=1
                    bit += bi
                    trit += tri
                    angt += ang
            dEMG = float(bit-trit)/line_count
            avgang = float(angt)/line_count
            return([dEMG,avgang])
        except FileNotFoundError:
            print("File does not exist")
        
        except:
            print("error occured")

    def get_fit(self):
        mat = []
        for i in range(9):
            fname = "file"+str(i+1)+".csv"
            mat.append(self.file_read(fname))
        mat = np.array(mat)
        print(np.array2string(mat))
        fit = self.data_fit(mat)
        name = 'fit'+time.strftime("%m%d%Y-%H%M%S")+'.txt'
        with open(name, 'w') as f:
            f.write(np.array2string(fit, separator=','))
        return fit
    

def main():
    exp = auto_exp()
    print(exp.get_fit())
    

if __name__ == '__main__':
    main()