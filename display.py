# -*- coding: utf-8 -*-
"""
Final project

Displayer
"""

import numpy as np
import matplotlib.pyplot as plt

class Display:
    def __init__(self):
        background = plt.imread('./images/bg.png')
        height,width,channel = background.shape
        dpi = plt.rcParams['figure.dpi']
        fig_size = height/dpi*60, width/dpi*60
        plt.figure(figsize=fig_size)
        ax = plt.axes([0,0,1,1], frameon=False)
        ax.set_axis_off()
        ax.set_xlim(0,10)
        ax.set_ylim(0,10)
        ax.imshow(background, origin='upper', extent=[0,10,0,10])
        
        self.cards = []
        for i in range(5):
            rows = []
            for j in range(5):
                item =  plt.imread('./images/back.png')
                x1 = 3.0+i*1.5#2.5+i*1.5
                x2 = 3.5+i*1.5#4.0+i*1.5
                y1 = 6.3-j*1.5#6.0-j*1.5
                y2 = 7.2-j*1.5#7.5-j*1.5
                rows.append(ax.imshow(item, origin='upper', extent=[x1,x2,y1,y2]))
            self.cards.append(rows)
        
        self.ations = []
    
    def show_card(self,row,col,face):
        self.cards[row][col].set_data(face)
    
    
'''
background = plt.imread('../bg.png')
height,width,channel = background.shape

item = plt.imread('../card_back.png')

dpi = plt.rcParams['figure.dpi']
fig_size = height/dpi*50, width/dpi*50

plt.figure(figsize=fig_size)
ax = plt.axes([0,0,1,1], frameon=False)
ax.set_axis_off()
ax.set_xlim(0,10)
ax.set_ylim(0,10)
im1 = ax.imshow(background, origin='upper', extent=[0,10,0,10])
im2 = ax.imshow(item, origin='upper', extent=[0,1.5,0,1.5])

plt.pause(1)
#new = plt.imread('../stereo.png')
new = np.zeros(item.shape)
im2.set_data(new)
'''
#screen = Display()
