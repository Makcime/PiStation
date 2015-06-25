#!/user/bin/env python

import time
import numpy as np
# import matplotlib.pyplot as plt
import smbus

# Special Chars
deg = u'\N{DEGREE SIGN}'

bus = smbus.SMBus(1)

# fig = plt.figure(' LM75 Temperatue Logger')

Timex = 100
Tempmin = 20
Tempmax = 25
elapsedtime = 0
tick = 0.5
# plt.axis([0, Timex, Tempmin, Tempmax])

i = 0
x = list()      
y = list()

# plt.ylabel('Temperature(Deg C)')
# plt.xlabel('Time(Seconds)')
# plt.ion()
# plt.show()

sensors = [0x49, 0x4c, 0x4f]

Oldtime = time.time()

for sensor in sensors:
    data = bus.read_i2c_block_data(sensor, 0)
    TempMSB = data[0]
    TempLSB = data[1]
    temp_y = (((TempMSB << 8) | TempLSB) >> 7) * 0.5
    if temp_y > 125:
        temp_y = (((((TempMSB << 8) | TempLSB) >> 7) * 0.5) - 256)
    if temp_y > Tempmax:
        Tempmax = temp_y + 2
        # plt.axis([0, Timex, Tempmin, Tempmax])
    if temp_y < Tempmin:
        Tempmin = temp_y - 2
        # plt.axis([0, Timex, Tempmin, Tempmax])
    if i > Timex * 0.75:
        Timex = Timex * 1.2
        # plt.axis([0, Timex, Tempmin, Tempmax])
    print "Temp on ", hex(sensor), ":",  temp_y, deg, "C"
    i = i + tick
    x.append(i)
    y.append(temp_y)
