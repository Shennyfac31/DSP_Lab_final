# -*- coding: utf-8 -*-
"""
Final project

Audio recording function
"""

import pyaudio
import numpy as np

CHUNK = 1024//2
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16
M_TH = 5
#En_Prm_TH = 10000#4500

silence_part = np.zeros(CHUNK)
speech_part = np.ones(CHUNK)

def get_digit():
    print("start recording")
    #txt.set_text("start recording")
    stop = 0
    silence = 0
    speech = 0
    speech_flag = 0
    total = 0
    
    #audio record
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    #print("start recording")
    
    data = stream.read(CHUNK)
    data = np.fromstring(data,'int16')
    frames = data
    status = silence_part
    mean = np.average(data)
    Emin = np.sum(np.abs(data-mean))
    En_TH = Emin*M_TH#En_Prm_TH*np.log10(Emin)
    
    while stop == 0:
        total = total+1
        data = stream.read(CHUNK)
        data = np.fromstring(data,'int16')
        frames = np.concatenate((frames,data))
        mean = np.average(data)
        Energy = np.sum(np.abs(data-mean))
        if (Energy-Emin)>=En_TH:
            speech = speech+1
            status = np.concatenate((status,speech_part))
            if speech>=5:
                silence = 0
                speech_flag = 1
                start_frame = total-10
        else:
            silence = silence+1
            status = np.concatenate((status,silence_part))
            #mean = np.average(data)
            #Emin = np.sum(np.abs(data-mean))
            #En_TH = En_Prm_TH*np.log10(Emin)
            if silence>=5:
                speech = 0
        if speech_flag==1 and silence>=5:
            stop = 1
        elif frames.size>RATE*3:
            #stop = 1
            frames = data
            status = silence_part
            silence = 0
            speech = 0
            speech_flag = 0
            total = 0
            mean = np.average(data)
            Emin = np.sum(np.abs(data-mean))
            En_TH = Emin*M_TH#En_Prm_TH*np.log10(Emin)
    
    #print("done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    print("done recording")
    #txt.set_text("done recording")
    start_frame = max(0,start_frame)
    start = start_frame*CHUNK
    
    return frames[start:]#, status[start:]


