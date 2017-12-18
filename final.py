# -*- coding: utf-8 -*-
"""
Final project

Main function
"""

import numpy as np
import matplotlib.pyplot as plt

import get_voice as gv
import recognition as rcg

f1,f2 = rcg.load_template()
fs = gv.RATE

for i in range(10):
    frames = gv.get_digit()
    digit,dis = rcg.test(frames,fs,f1,f2)
    print((digit,dis))
    #plt.pause(1)
    #plt.figure()
    #plt.plot(frames)
    #plt.plot(status)
    #plt.show()

#time = np.arange(frames.size)/sf
#plt.figure(1)
#plt.plot(time,frames)