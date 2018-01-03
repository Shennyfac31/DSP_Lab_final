# -*- coding: utf-8 -*-
"""
Final project

Play game
"""

import numpy as np
import matplotlib.pyplot as plt
import random

import display

class Card:
    def __init__(self, ele, pt):
        self.status = 'normal'
        self.element = ele
        self.point = pt

class Game:
    def __init__(self):
        deck = []
        for element in ['fire','air','water','earth','special']:
            for i in range(5):
                deck.append(Card(element,i))
        random.shuffle(deck)
        self.deck = np.array(deck).reshape((5,5))
        self.menu = ['flip','tool','hint','quit']
        self.tools = ['out']
        self.stk = ['eye','frog','rabbit','bomb','shield']
        self.screen = display.Display()
        self.state = 'initial'
        self.action = None
        self.flipped_row = None
        self.flipped_col = None
        self.end_game = False
        self.score = 0
        self.bonus = 0
        self.malus = 0
        self.hint_count = 0
        self.menu_ptr = 0
        self.tools_ptr = 0
        self.row_ptr = 0
        self.col_ptr = 0
        self.counter = 0
        self.txt = plt.text(0.5, 8, '', fontsize=30, color='r')
    
    def view_all(self, odd=None):
        for i in range(5):
            for j in range(5):
                if odd is None:
                    if self.deck[i,j].status=='normal':
                        self.screen.show_card_face(i, j, self.deck[i,j].element, 
                                                   self.deck[i,j].point)
                else:
                    if (i+j)%2==odd and self.deck[i,j].status=='normal':
                        self.screen.show_card_face(i, j, self.deck[i,j].element, 
                                                   self.deck[i,j].point)
    
    def hide_all(self):
        for i in range(5):
            for j in range(5):
                self.screen.show_card_back(i, j, self.deck[i,j].status)
    
    def control(self, command):
        self.txt.set_text('')
        if self.state == 'initial':
            self.step_initial(command)
        elif self.state == 'menu':
            self.step_menu(command)
        elif self.state == 'flip':
            self.step_flip(command)
        elif self.state == 'tool':
            self.step_tool(command)
        elif self.state == 'hint':
            self.step_hint(command)
        else:
            print('Error: No game state')
    
    def step_initial(self, move):
        if move==1 or move==3:
            self.menu_ptr = 3
            self.screen.select_action(self.menu_ptr)
            self.state = 'menu'
        elif move==2 or move==4:
            self.screen.select_action(self.menu_ptr)
            self.state = 'menu'
        elif move==0:
            #print('Try something else')
            self.txt.set_text('Try something else.')
        else:
            print('Error: Command error')
    
    def step_menu(self, move):
        if move==1 or move==3:
            self.screen.unselect_action(self.menu_ptr)
            self.menu_ptr = (self.menu_ptr+3)%4
            self.screen.select_action(self.menu_ptr)
            self.state = 'menu'
        elif move==2 or move==4:
            self.screen.unselect_action(self.menu_ptr)
            self.menu_ptr = (self.menu_ptr+1)%4
            self.screen.select_action(self.menu_ptr)
            self.state = 'menu'
        elif move==0:
            self.screen.unselect_action(self.menu_ptr)
            self.state = self.menu[self.menu_ptr]
            if self.state == 'quit':
                self.end_game = True
            elif self.state == 'tool':
                self.tools_ptr = 0
                self.screen.show_tool(self.tools_ptr, 'select', self.tools[self.tools_ptr])
            else:
                self.row_ptr = 0
                self.col_ptr = 0
                self.deck[self.row_ptr,self.col_ptr].status += '_s'
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
        else:
            print('Error: Command error')
    
    def step_flip(self, move):
        if self.flipped_row is None:
            if move==0:
                if self.deck[self.row_ptr,self.col_ptr].status=='void_s':
                    #print('This one is done')
                    self.txt.set_text('This one is done.')
                    self.state = 'flip'
                elif self.deck[self.row_ptr,self.col_ptr].element=='special':
                    p = self.deck[self.row_ptr,self.col_ptr].point
                    self.tools.append(self.stk[p])
                    idx = len(self.tools)-1
                    self.screen.show_tool(idx, 'normal', self.tools[idx])
                    self.screen.show_card_face(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].element, 
                                               self.deck[self.row_ptr,self.col_ptr].point)
                    self.screen.delay()
                    self.deck[self.row_ptr,self.col_ptr].status = 'void'
                    self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].status)
                    self.counter += 1
                    if self.counter==25:
                        self.end_game = True
                    self.state = 'menu'
                    self.menu_ptr = 0
                    self.screen.select_action(self.menu_ptr)
                else:
                    self.flipped_row = self.row_ptr
                    self.flipped_col = self.col_ptr
                    self.screen.show_card_face(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].element, 
                                               self.deck[self.row_ptr,self.col_ptr].point)
                    self.state = 'flip'
            else:
                self.choose_card(move)
                self.state = 'flip'
        else:
            if move==0:
                if (self.flipped_row == self.row_ptr 
                and self.flipped_col == self.col_ptr):
                    #print('Cannot choose the same card')
                    self.txt.set_text('Already chosen.')
                    self.state = 'flip'
                elif self.deck[self.row_ptr,self.col_ptr].status=='void_s':
                    #print('This one is done')
                    self.txt.set_text('This one is done.')
                    self.state = 'flip'
                elif self.deck[self.row_ptr,self.col_ptr].element=='special':
                    self.screen.show_card_face(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].element, 
                                               self.deck[self.row_ptr,self.col_ptr].point)
                    self.screen.delay()
                    self.deck[self.row_ptr,self.col_ptr].status = 'void'
                    self.deck[self.flipped_row,self.flipped_col].status = 'normal'
                    self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].status)
                    self.screen.show_card_back(self.flipped_row, self.flipped_col, 
                                               self.deck[self.flipped_row,self.flipped_col].status)
                    self.flipped_row = None
                    p = self.deck[self.row_ptr,self.col_ptr].point
                    self.special_card(self.stk[p])
                    self.counter += 1
                    if self.counter==25:
                        self.end_game = True
                    self.state = 'menu'
                    self.menu_ptr = 0
                    self.screen.select_action(self.menu_ptr)
                else:
                    self.screen.show_card_face(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].element, 
                                               self.deck[self.row_ptr,self.col_ptr].point)
                    self.screen.delay()
                    if (self.deck[self.flipped_row,self.flipped_col].point 
                    == self.deck[self.row_ptr,self.col_ptr].point):
                        self.score += (10+self.bonus*10)
                        self.bonus = self.bonus//2
                        self.deck[self.flipped_row,self.flipped_col].status = 'void'
                        self.deck[self.row_ptr,self.col_ptr].status = 'void'
                        self.counter += 2
                        if self.counter==25:
                            self.end_game = True
                    else:
                        self.score -= (3+self.malus*3)
                        self.malus = self.malus//2
                        self.deck[self.flipped_row,self.flipped_col].status = 'normal'
                        self.deck[self.row_ptr,self.col_ptr].status = 'normal'
                    self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].status)
                    self.screen.show_card_back(self.flipped_row, self.flipped_col, 
                                               self.deck[self.flipped_row,self.flipped_col].status)
                    self.flipped_row = None
                    self.state = 'menu'
                    self.menu_ptr = 0
                    self.screen.select_action(self.menu_ptr)
            else:
                self.choose_card(move)
                self.state = 'flip'
    
    def step_hint(self, move):
        self.hint_count = (self.hint_count+1)%5
        if move==0:
            if self.deck[self.row_ptr,self.col_ptr].status=='void_s':
                #print('This one is done')
                self.txt.set_text('This one is done.')
                self.state = 'hint'
            else:
                if self.hint_count==0:
                    self.screen.show_card_back(self.row_ptr, self.col_ptr, 'mischief')
                else:
                    self.screen.show_card_face(self.row_ptr, self.col_ptr, 
                                               self.deck[self.row_ptr,self.col_ptr].element, 
                                               self.deck[self.row_ptr,self.col_ptr].point)
                self.screen.delay()
                self.deck[self.row_ptr,self.col_ptr].status = 'normal'
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
                self.score -= 1
                self.state = 'menu'
                self.menu_ptr = 0
                self.screen.select_action(self.menu_ptr)
        else:
            self.choose_card(move)
            self.state = 'hint'
    
    def step_tool(self, move):
        if move==1 or move==3:
            num = len(self.tools)
            self.screen.show_tool(self.tools_ptr, 'normal', self.tools[self.tools_ptr])
            self.tools_ptr = (self.tools_ptr+num-1)%num
            self.screen.show_tool(self.tools_ptr, 'select', self.tools[self.tools_ptr])
            self.state = 'tool'
        elif move==2 or move==4:
            num = len(self.tools)
            self.screen.show_tool(self.tools_ptr, 'normal', self.tools[self.tools_ptr])
            self.tools_ptr = (self.tools_ptr+1)%num
            self.screen.show_tool(self.tools_ptr, 'select', self.tools[self.tools_ptr])
            self.state = 'tool'
        elif move==0:
            if self.tools_ptr>0:
                selected_tool = self.tools.pop(self.tools_ptr)
                if selected_tool=='eye':
                    self.view_all()
                    self.screen.delay()
                    self.hide_all()
                elif selected_tool=='frog':
                    self.view_all(odd=1)
                    self.screen.delay()
                    self.hide_all()
                elif selected_tool=='rabbit':
                    self.view_all(odd=0)
                    self.screen.delay()
                    self.hide_all()
                elif selected_tool=='bomb':
                    self.bonus = 8
                elif selected_tool=='shield':
                    self.malus = 0
            for i in range(self.tools_ptr,len(self.tools)):
                self.screen.show_tool(self.tools_ptr, 'normal', self.tools[self.tools_ptr])
            self.screen.hide_tool(len(self.tools))
            self.state = 'menu'
            self.menu_ptr = 0
            self.screen.select_action(self.menu_ptr)
        else:
            print('Error: Command error')
    
    def choose_card(self, move):
        if move==3:
            st = self.deck[self.row_ptr,self.col_ptr].status
            self.deck[self.row_ptr,self.col_ptr].status = st.replace('_s','')
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
            self.row_ptr = (self.row_ptr+4)%5
            self.deck[self.row_ptr,self.col_ptr].status += '_s'
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
        elif move==4:
            st = self.deck[self.row_ptr,self.col_ptr].status
            self.deck[self.row_ptr,self.col_ptr].status = st.replace('_s','')
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
            self.row_ptr = (self.row_ptr+1)%5
            self.deck[self.row_ptr,self.col_ptr].status += '_s'
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
        elif move==1:
            st = self.deck[self.row_ptr,self.col_ptr].status
            self.deck[self.row_ptr,self.col_ptr].status = st.replace('_s','')
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
            self.col_ptr = (self.col_ptr+4)%5
            self.deck[self.row_ptr,self.col_ptr].status += '_s'
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
        elif move==2:
            st = self.deck[self.row_ptr,self.col_ptr].status
            self.deck[self.row_ptr,self.col_ptr].status = st.replace('_s','')
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
            self.col_ptr = (self.col_ptr+1)%5
            self.deck[self.row_ptr,self.col_ptr].status += '_s'
            if (self.flipped_row != self.row_ptr or self.flipped_col != self.col_ptr):
                self.screen.show_card_back(self.row_ptr, self.col_ptr, 
                                           self.deck[self.row_ptr,self.col_ptr].status)
        else:
            print('Error: Choose card error')
    
    def special_card(self, card_act):
        if card_act=='eye':
            self.deck = self.deck.T
            self.hide_all()
        elif card_act=='frog':
            np.random.shuffle(self.deck)
            self.hide_all()
        elif card_act=='rabbit':
            self.deck = self.deck.T
            np.random.shuffle(self.deck)
            self.deck = self.deck.T
            self.hide_all()
        elif card_act=='bomb':
            self.malus = 8
        elif card_act=='shield':
            self.bonus = 0
        else:
            print('Error: Special card unfound')
    
    def starting(self, page):
        self.screen.change_cover(page)
    
    def ending(self):
        if self.score>200:
            self.screen.change_cover('end_high')
        elif self.score>0:
            self.screen.change_cover('end_mid')
        else:
            self.screen.change_cover('end_low')

