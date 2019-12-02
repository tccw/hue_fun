"""
A better candle scene
"""

import numpy as np
from phue import Bridge
from math import ceil

b = Bridge('192.168.1.64') # your bridge IP here
b.connect()

lr_lamp = [1,4]
b.set_light(lr_lamp, 'on', True)
b.set_light(lr_lamp, 'ct', 380, transitiontime = 0) # set color temp.

m = 1.5 # brightness multiplier

while True:

    pchance = np.random.uniform(0,1)


    if pchance <= 0.005: # one percent chance of gusty breeze
        n = 0
        n_flickers = np.random.randint(2,6)

        while n < n_flickers:
            t0 = np.random.randint(0.5,2)
            t1 = np.random.randint(0.5,2)
            bri_val_f0 = np.random.randint(60,120)
            bri_val_f1 = np.random.randint(60,120)

            b.set_light(lr_lamp[0], 'bri', ceil(bri_val_f0 * m), transitiontime = t0)
            b.set_light(lr_lamp[1], 'bri', ceil(bri_val_f1 * m), transitiontime = t1)

            n = n + 1
    else:
        t0 = np.random.randint(3,8)
        t1 = np.random.randint(3,8)
        bri_val_f0 = np.random.randint(80,110)
        bri_val_f1 = np.random.randint(80,110)

        b.set_light(lr_lamp[0], 'bri', ceil(bri_val_f0 * m), transitiontime = t0)
        b.set_light(lr_lamp[1], 'bri', ceil(bri_val_f1 * m), transitiontime = t1)
