import serial
import time

ser = serial.Serial(port = '/dev/ttyUSB0',
                    baudrate = 115200,
                    bytesize = serial.EIGHTBITS,
                    parity = serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout = 0.5)
command_char = '$'
command_group_1 = '0'
command_group_1_list = [0,1,2,3]
ser.write_timeout = 0.5
for e in command_group_1_list:
    #estr = str(command_char+command_group_1+' '+'1'+'\r\n')
    estr = '$ 0 2'
    bstr = str.encode(estr)
    print(bstr.decode())
    ser.write(bstr)
    time.sleep(1)

ser.close()