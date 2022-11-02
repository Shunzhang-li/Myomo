import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import sys


class serial_plotter:

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
        self.fig = None
        self.subfig = None

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


    def animate(fig, i, xs, ys, name, self):
        while True:
            line = self.ser.readline().decode("utf-8")
            line_as_list = line.split(',')
            if line_as_list[0] == '\x00E':
                break

            
        print('line: ' + line + '\n')

        print('line list: ' + '\n')
        print(line_as_list)
        print('\n')
        data = float(line_as_list[self.dict[name]].split('\n')[0])
        print("\ndata: "+str(line_as_list[self.dict[name]])+"\n")
        i = round(float(line_as_list[self.dict['Time']].split('\n')[0]),2)
        xs.append(i)
        ys.append(data) 

        #limit xy list length
        length = 20
        xs = xs[-length:]
        ys = ys[-length:]

        self.subfig.clear()

        self.subfig.plot(xs,ys)
        #plt.legend()
        plt.xlabel("time")
        plt.ylabel(name)

    def start_plot(self, name = 'Joint Position'):
        self.fig = plt.figure()
        self.subfig = self.fig.add_subplot(1,1,1)
        xs = []
        ys = []
        try:
            index = self.dict[name]
            ani = animation.FuncAnimation(self.fig,self.animate,fargs=(xs,ys,name,self),interval = 1000)
            plt.show()
        except KeyError:
            #print('Name wrong, plotting Joint Position')
            name = 'Joint Position'
            ani = animation.FuncAnimation(self.fig,self.animate,fargs=(xs,ys,name,self),interval = 1000)
            plt.show()
        except:
            print("plotter failed")

    def tear_down(self):
        self.ser.close()

def main(argv):
    plotter = serial_plotter()
    plotter.start_plot(argv)

if __name__ == '__main__':
    main(sys.argv[0])