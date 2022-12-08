#comment
import serial
import time
ser = serial.Serial(port = '/dev/ttyUSB0',
                    baudrate = 115200,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout = 0.5)
count = 1
seq = []
while True:
    for c in ser.read():
        seq.append(chr(c)) #convert from ANSII
        joined_seq = ''.join(str(v) for v in seq) #Make a string from array

        if chr(c) == '\n':
            #print("Line " + str(count) + ': ' + joined_seq)
            JA = joined_seq.split(',')
            ct = time.time()
            #print(str(ct)+ ' '+JA[14])
            seq = []
            count += 1
            
            print(str(ct)+ ' '+JA[14])
            #time.sleep(0.1)
            break
        
        #time.sleep(0.1)
ser.close()