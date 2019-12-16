import numpy as np
from phue import Bridge
import datetime
import time
from math import floor

b = Bridge('192.168.1.64') # your bridge IP here
b.connect()

lr_lamp = [1,4]
b.set_light(lr_lamp, 'on', True)
b.set_light(lr_lamp[0], 'xy', [0.3,1.])
b.set_light(lr_lamp[1], 'xy', [1., 0.2])
x = np.pi
step = 0.01

while True:
    x = x + step
    bri_val = np.power(2, np.cos(x) + 1) * 50
    b.set_light(lr_lamp, 'bri', floor(bri_val) , transitiontime = 1)
