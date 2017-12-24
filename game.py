# -*- coding: utf-8 -*-
"""
Final project

Play game
"""

import numpy as np
import matplotlib.pyplot as plt
import random

import display

def load_back():
    card_back = {}
    card_back['normal'] = plt.imread('./images/back.png')
    card_back['select'] = plt.imread('./images/select.png')
    card_back['frog'] = plt.imread('./images/frog.png')
    card_back['fire'] = plt.imread('./images/fire.png')
    card_back['air'] = plt.imread('./images/air.png')
    card_back['water'] = plt.imread('./images/water.png')
    card_back['earth'] = plt.imread('./images/earth.png')
    card_back['none'] = np.zeros(card_back['normal'].shape)
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

class Card:
    def __init__(self, ele, pt):
        self.status = 'normal'
        self.element = ele
        self.point = pt

class Game:
    def __init__(self):
        self.card_backs = load_back()
        self.card_faces = load_face()
        deck = []
        for element in ['fire','air','water','earth','special']:
            for i in range(5):
                deck.append(Card(element,i))
        random.shuffle(deck)
        self.deck = np.array(deck).reshape((5,5))
        self.screen = display.Display()
        
    def view_all(self):
        for i in range(5):
            for j in range(5):
                element = self.deck[i,j].element
                point = self.deck[i,j].point
                face = self.card_faces[element][point]
                self.screen.show_card(i, j, face)

