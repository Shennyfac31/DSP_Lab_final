# -*- coding: utf-8 -*-
"""
Final project

Record templates
"""

import wave

import get_voice as gv

WAVE_OUTPUT_FILENAME = "./train/n3.wav"
CHUNK = 1024
CHANNELS = 1
RATE = 16000
WIDTH = 2

frames = gv.get_digit()

filename = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
filename.setnchannels(CHANNELS)
filename.setsampwidth(WIDTH)
filename.setframerate(RATE)
filename.writeframes(frames)
filename.close()
'''
for i in range(6):
    frames = gv.get_digit()
    
    filename = wave.open('./'+str(i)+'.wav', 'wb')
    filename.setnchannels(CHANNELS)
    filename.setsampwidth(WIDTH)
    filename.setframerate(RATE)
    filename.writeframes(frames)
    filename.close()
'''
    