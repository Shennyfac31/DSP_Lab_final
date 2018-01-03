# -*- coding: utf-8 -*-
"""
Final project

Displayer
"""

import numpy as np
import matplotlib.pyplot as plt

def load_back():
    card_back = {}
    card_back['normal'] = plt.imread('./images/back.png')
    card_back['normal_s'] = plt.imread('./images/select.png')
    card_back['void'] = np.zeros(card_back['normal'].shape)
    card_back['void_s'] = plt.imread('./images/select_void.png')
    card_back['mischief'] = plt.imread('./images/mischief.png')
    return card_back

def load_face():
    card_face = {}
    for element in ['fire','air','water','earth','special']:
        list_pt = []
        addr = './images/'+element
        for i in range(5):
            list_pt.append(plt.imread(addr+str(i+1)+'.png'))
        card_face[element] = list_pt
    return card_face

def load_action():
    normal = {'flip': plt.imread('./images/flip.png'), 
              'tool': plt.imread('./images/tool.png'), 
              'hint': plt.imread('./images/hint.png'), 
              'quit': plt.imread('./images/quit.png')}
    select = {'flip': plt.imread('./images/flip_s.png'), 
              'tool': plt.imread('./images/tool_s.png'), 
              'hint': plt.imread('./images/hint_s.png'), 
              'quit': plt.imread('./images/quit_s.png')}
    action = {'normal': normal, 
              'select': select}
    return action

def load_tool():
    normal = {'out': plt.imread('./images/out.png'), 
              'frog': plt.imread('./images/frog.png'), 
              'bomb': plt.imread('./images/bomb.png'), 
              'eye': plt.imread('./images/eye.png'), 
              'rabbit': plt.imread('./images/rabbit.png'), 
              'shield': plt.imread('./images/shield.png')}
    select = {'out': plt.imread('./images/out_s.png'), 
              'frog': plt.imread('./images/frog_s.png'), 
              'bomb': plt.imread('./images/bomb_s.png'), 
              'eye': plt.imread('./images/eye_s.png'), 
              'rabbit': plt.imread('./images/rabbit_s.png'), 
              'shield': plt.imread('./images/shield_s.png')}
    tool = {'normal': normal, 
            'select': select}
    return tool

def load_covers():
    covers = {'start': plt.imread('./images/start.png'), 
              'rec_up': plt.imread('./images/rec_up.png'), 
              'rec_down': plt.imread('./images/rec_down.png'), 
              'rec_left': plt.imread('./images/rec_left.png'), 
              'rec_right': plt.imread('./images/rec_right.png'), 
              'rec_hit': plt.imread('./images/rec_hit.png'), 
              'go': plt.imread('./images/go.png'), 
              'end_high': plt.imread('./images/end_high.png'), 
              'end_mid': plt.imread('./images/end_mid.png'), 
              'end_low': plt.imread('./images/end_low.png'), 
              'hide': np.zeros((10,10,4))}
    return covers

class Display:
    def __init__(self):
        background = plt.imread('./images/bg.png')
        height,width,channel = background.shape
        dpi = plt.rcParams['figure.dpi']
        fig_size = height/dpi, width/dpi
        plt.figure(figsize=fig_size)
        ax = plt.axes([0,0,1,1], frameon=False)
        ax.set_axis_off()
        ax.set_xlim(0,10)
        ax.set_ylim(0,10)
        ax.imshow(background, origin='upper', extent=[0,10,0,10])
        
        self.card_backs = load_back()
        self.card_faces = load_face()
        self.cards = []
        for i in range(5):
            rows = []
            for j in range(5):
                item = self.card_backs['normal']
                x1 = 3.0+i*1.5
                x2 = 3.5+i*1.5
                y1 = 6.3-j*1.5
                y2 = 7.2-j*1.5
                rows.append(ax.imshow(item, origin='upper', extent=[x1,x2,y1,y2]))
            self.cards.append(rows)
        
        self.action_bar = load_action()
        self.action_list = ['flip','tool','hint','quit']
        self.ations = []
        for j in range(4):
            key = self.action_list[j]
            item = self.action_bar['normal'][key]
            x1 = 0.5
            x2 = 2.5
            y1 = 6.3-j*1.0
            y2 = 7.0-j*1.0
            self.ations.append(ax.imshow(item, origin='upper', extent=[x1,x2,y1,y2]))
        
        self.tool_bar = load_tool()
        self.tool_hide = np.zeros((10,10,4))
        self.tools = []
        for i in range(6):
            if i==0:
                item = self.tool_bar['normal']['out']
            else:
                item = self.tool_hide
            x1 = 0.0+i*1.0
            x2 = 1.0+i*1.0
            y1 = 9.0
            y2 = 10.0
            self.tools.append(ax.imshow(item, origin='upper', extent=[x1,x2,y1,y2]))
        
        self.fill = load_covers()
        self.cover = ax.imshow(self.fill['start'], origin='upper', extent=[0,10,0,10])
    
    def show_card_face(self, row, col, element, point):
        self.cards[row][col].set_data(self.card_faces[element][point])
    
    def show_card_back(self, row, col, status):
        self.cards[row][col].set_data(self.card_backs[status])
    
    def select_action(self, index):
        key = self.action_list[index]
        self.ations[index].set_data(self.action_bar['select'][key])
    
    def unselect_action(self, index):
        key = self.action_list[index]
        self.ations[index].set_data(self.action_bar['normal'][key])
    
    def show_tool(self, index, status, tool):
        self.tools[index].set_data(self.tool_bar[status][tool])
    
    def hide_tool(self, index):
        self.tools[index].set_data(self.tool_hide)
    
    def change_cover(self, cover_name):
        self.cover.set_data(self.fill[cover_name])
    
    def delay(self, sec=1):
        plt.pause(sec)

