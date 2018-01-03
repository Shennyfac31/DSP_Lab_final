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

fs = gv.RATE

core = game.Game()
txt = plt.text(1, 1, 'Ready? The recording will start in 5 sec.', fontsize=25, color='r')
core.screen.delay(1)
for i in range(4):
    txt.set_text('Ready? The recording will start in '+str(4-i)+' sec.')
    core.screen.delay(1)

txt.set_text('')
template = []
for move in ['hit','up','down','left','right']:
    core.starting('rec_'+move)
    core.screen.delay(0.01)
    frames = gv.get_digit()
    feat = rcg.template(frames,fs)
    template.append(feat)

txt.set_position((9.5,8))
txt.set_fontsize(50)
txt.set_family('serif')
txt.set_color('black')
txt.set_ha('right')
core.starting('go')
core.screen.delay(0.3)
core.starting('hide')
core.screen.delay(0.01)

while core.end_game is False:
    frames = gv.get_digit()
    digit,dis = rcg.test(frames,fs,template)
    print((digit,dis))
    core.control(digit)
    txt.set_text('Score: '+str(core.score))
    core.screen.delay(0.01)

core.ending()
txt.set_position((5,2))
txt.set_fontsize(30)
txt.set_family('monospace')
txt.set_ha('center')
txt.set_text('Total score: '+str(core.score))
core.screen.delay(0.01)

