#!/usr/bin/env python

import sys
import serial
from time import sleep


# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/' + sys.argv[1]
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 115200

ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)

pin = sys.argv[2] #intakes the pin 

openPin = 'AT+CPIN="%s"\r' % pin
removePin = 'AT+CLCK="SC",0,"%s"\r' % pin
askPin = 'AT+CPIN?\r'

def main():
    if not ser.is_open:
        ser.open()

    if ser.is_open:
        print "OPEN OK !"
        
        ser.write(askPin.encode('ascii'))       #Asks status of SIM, If locked returns +CPIN: SIM PIN else +CPIN: READY
        sleep(0.5)
        readOutput()

        
        ser.write(openPin.encode('ascii'))      #AT+CPIN= XXXX opens SIM with pin
        sleep(0.5)
        readOutput()

        ser.write(removePin.encode('ascii'))    #Removes PIN from SIM card
        sleep(0.5)
        readOutput()          

        ser.write(askPin.encode('ascii'))
        sleep(0.5)
        readOutput()
        
        ser.close()

def readOutput():
    print ser.read_all().decode()

if __name__ == "__main__":
    try: 
        main()
    except Exception as e:
        print 'Error: ' + str(e)