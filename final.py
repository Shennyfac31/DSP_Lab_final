# -*- coding: utf-8 -*-
"""
Final project

Main function
"""

import numpy as np
import matplotlib.pyplot as plt

import get_voice as gv
import recognition as rcg
import game

f1,f2 = rcg.load_template()
fs = gv.RATE

core = game.Game()
core.screen.delay(0.1)
txt = plt.text(3.5, 7.5, "", fontsize=30, color='r')
while core.end_game is False:
    frames = gv.get_digit()
    digit,dis = rcg.test(frames,fs,f1,f2)
    print((digit,dis))
    core.control(digit)
    txt.set_text('Cards: '+str(core.counter)+', Score: '+str(core.score))
    core.screen.delay(0.1)
'''
f1,f2 = rcg.load_template()
fs = gv.RATE

fig = plt.figure(1, figsize=(10,6))
for i in range(10):
    frames,status = gv.get_digit()
    #digit,dis = rcg.test(frames,fs,f1,f2)
    #print((digit,dis))
    fig.clear()
    plt.plot(frames)
    plt.plot(status*max(frames)/2)
    plt.show()
    plt.pause(1)
'''
#time = np.arange(frames.size)/sf
#plt.figure(1)
#plt.plot(time,frames)