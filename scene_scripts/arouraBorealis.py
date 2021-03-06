# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 15:48:29 2018

@author: tccw
"""
import numpy as np
from phue import Bridge
import datetime
import time

b = Bridge('192.168.1.64') # your bridge IP here
b.connect()

lr_lamp = [1,4]
b.set_light(lr_lamp, 'on', True)
n = 0
nrun = 20   # number of cycles

#while (n < nrun):
while True:
    bri_val_f = np.random.randint(20,180) # Random brightness
   #bri_val_s = np.int(np.random.uniform(0.,1.)*bri_val_f)
    t = np.random.randint(15,500) # Random transition time in seconds
    pchance = np.random.uniform(0,1)

    #pchance = np.random.random() # Random number to determine chance of occurance
    tnow = datetime.datetime.now()

    if tnow.hour >= 17 or tnow.hour <= 5: # Blue is only seen on the dark side of the earth

        if pchance < 0.1: #set red and green
            b.set_light(lr_lamp,'bri',bri_val_f, transitiontime = t)
            b.set_light(lr_lamp[0], 'xy', [0.3,1.], transitiontime = t)
            b.set_light(lr_lamp[1], 'xy', [1.,0.2], transitiontime = t/2)
            time.sleep(t/10)
        if pchance < 0.15: # set blueish
            b.set_light(lr_lamp,'bri',bri_val_f, transitiontime = t)
            b.set_light(lr_lamp, 'xy', [0.,0.], transitiontime = t/2)
            time.sleep(t/10)
        if pchance < 0.75: #set green
            b.set_light(lr_lamp,'bri',bri_val_f, transitiontime = t)
            b.set_light(lr_lamp, 'xy', [0.3,1.], transitiontime = t/2)
            time.sleep(t/10)
    else:

        if pchance < 0.2: #set red and green
            b.set_light(lr_lamp,'bri',bri_val_f, transitiontime = t)
            b.set_light(lr_lamp[0], 'xy', [0.3,1.], transitiontime = t)
            b.set_light(lr_lamp[1], 'xy', [1.,0.2], transitiontime = t/2)
            time.sleep(t/10)
        if pchance < 0.8: #set green
            b.set_light(lr_lamp,'bri',bri_val_f, transitiontime = t)
            b.set_light(lr_lamp, 'xy', [0.3,1.], transitiontime = t/2)
            time.sleep(t/10)
    #n = n + 1
