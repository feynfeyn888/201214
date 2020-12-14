import numpy as np
from sense_hat import SenseHat

import serial
import time

sense = SenseHat()

# serial takes these two parameters: serial device and baudrate(変調回数)
ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    data = []
    for index in range(0, 10):
        datum = ser.read()
        # print(datum)
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    print('pmtwofive:', pmtwofive)
    print('pmten:', pmten)

    time.sleep(1)

    e = [0,0,0]
    w = [255, 255, 255]

    z4 = [
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        w,w,w,w,w,w,w,w,
        ]

    sense.set_pixels(z4)
    time.sleep(2)
    sense.clear()