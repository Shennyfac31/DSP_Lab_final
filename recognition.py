# -*- coding: utf-8 -*-
"""
Final project

Digit recognition
"""

import numpy as np
import soundfile as sf

import MFCC
import DTW

Frame_Len = 320
Hop_Len = 160

def load_template():
    feat1 = []
    feat2 = []
    
    for i in range(0,5):
        signal,fs = sf.read('./train/n'+str(i)+'.wav')
        mean = np.average(signal)
        energy = np.sum(np.abs(signal-mean))
        signal = signal/energy*100
        mfcc = MFCC.MFCC(signal,fs,Frame_Len,Hop_Len)
        feat1.append(mfcc)
        
#        signal,fs = sf.read('./train/w'+str(i)+'.wav')
#        mean = np.average(signal)
#        energy = np.sum(np.abs(signal-mean))
#        signal = signal/energy*100
#        mfcc = MFCC.MFCC(signal,fs,Frame_Len,Hop_Len)
#        feat2.append(mfcc)
    
    return feat1, feat2

def test(signal,fs,feat1,feat2):
    mean = np.average(signal)
    energy = np.sum(np.abs(signal-mean))
    signal = signal/energy*100
    
    mfcc = MFCC.MFCC(signal,fs,Frame_Len,Hop_Len)
    digit = 0
    c1 = DTW.DTW(mfcc,feat1[0])
    #c2 = DTW.DTW(mfcc,feat2[0])
    dis = c1#min(c1,c2)+0.3*max(c1,c2)
    
    for i in range(0,len(feat1)):
        c1 = DTW.DTW(mfcc,feat1[i])
        #c2 = DTW.DTW(mfcc,feat2[i])
        c = c1#min(c1,c2)+0.3*max(c1,c2)
        if c<dis:
            digit = i
            dis = c
    
    return digit, dis

