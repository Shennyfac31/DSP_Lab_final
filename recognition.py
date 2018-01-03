# -*- coding: utf-8 -*-
"""
Final project

Digit recognition
"""

import numpy as np

import MFCC
import DTW

Frame_Len = 320
Hop_Len = 160

def template(signal, fs):
    mean = np.average(signal)
    energy = np.sum(np.abs(signal-mean))
    signal = signal/energy*100
    mfcc = MFCC.MFCC(signal,fs,Frame_Len,Hop_Len)    
    return mfcc

def test(signal, fs, feat_list):
    mean = np.average(signal)
    energy = np.sum(np.abs(signal-mean))
    signal = signal/energy*100
    
    mfcc = MFCC.MFCC(signal,fs,Frame_Len,Hop_Len)
    digit = 0
    c = DTW.DTW(mfcc,feat_list[0])
    dis = c
    
    for i in range(0,len(feat_list)):
        c = DTW.DTW(mfcc,feat_list[i])
        if c<dis:
            digit = i
            dis = c
    
    return digit, dis


