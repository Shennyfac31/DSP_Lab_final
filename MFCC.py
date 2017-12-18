# -*- coding: utf-8 -*-
"""
Final project

MFCC function
"""

import numpy as np
import math
from scipy.fftpack import dct
from scipy import signal as sg

#MFCC
def pre_emphasis(signal,coefficient=0.95):
    return np.append(signal[0],signal[1:]-coefficient*signal[:-1])

def mel2hz(mel):
    '''
    mel scale to Hz scale
    '''
    hz = (10**(mel/2595.0)-1)*700
    return hz

def hz2mel(hz):
    '''
    hz scale to mel scale
    '''
    mel = 2595*math.log10(1+hz/700.0)
    return mel

def get_filter_banks(filters_num,NFFT,samplerate,low_freq=0,high_freq=None):
    ''' Mel Bank
    filers_num: filter numbers
    NFFT:points of your FFT
    samplerate:sample rate
    low_freq: the lowest frequency that mel frequency include
    high_freq:the Highest frequency that mel frequency include
    '''
    #turn the hz scale into mel scale
    low_mel=hz2mel(low_freq)
    high_mel=hz2mel(high_freq)
    #in the mel scale, you should put the position of your filter number 
    mel_points=np.linspace(low_mel,high_mel,filters_num+2)
    #get back the hzscale of your filter position
    hz_points=mel2hz(mel_points)
    #Mel triangle bank design
    center=np.floor((NFFT+1)*hz_points/samplerate)
    fbank=np.zeros([filters_num,int(NFFT/2+1)])
    
    for i in range(0,filters_num):
        start = int(center[i])
        end = int(center[i+2])
        tri_wid = end-start
        tri_fil = sg.bartlett(tri_wid,sym=False)
        fbank[i][start:end] = tri_fil
    
    return fbank

def MFCC(signal,fs,frame_length,frame_step):
    '''
    NFFT:     points of your FFT, NFFT/2+1 is the final #pts
    low_freq: the lowest frequency that mel frequency include
    high_freq:the Highest frequency that mel frequency include
    '''
    NFFT=1300
    low_freq=0
    high_freq=int(fs/2)
    
    signal_length=len(signal)
    filters_num=26

    emphasis_coeff=0.95
    signal_p=pre_emphasis(signal,emphasis_coeff)

    frames_num=1+int(math.ceil((1.0*signal_length-frame_length)/frame_step))
    
    #padding    
    pad_length=int((frames_num-1)*frame_step+frame_length)
    zeros=np.zeros((pad_length-signal_length,))   
    pad_signal=np.concatenate((signal_p,zeros))
    
    #split into frames
    indices=(np.tile(np.arange(0,frame_length),(frames_num,1))+
             np.tile(np.arange(0,frames_num*frame_step,frame_step),(frame_length,1)).T)
    indices=np.array(indices,dtype=np.int32)
    frames=pad_signal[indices]
    frames *= np.hamming(frame_length)
    
    ###complex_spectrum=np.fft.rfft(frames,NFFT).T
    complex_spectrum=np.fft.rfft(frames,NFFT)
    absolute_complex_spectrum=np.abs(complex_spectrum)**2
    
    fb=get_filter_banks(filters_num,NFFT,fs,low_freq,high_freq) 
    #plt.figure(1)
    #plt.plot(fb.T)
    
    ###mel_energy = np.dot(fb,absolute_complex_spectrum)
    mel_energy = np.dot(absolute_complex_spectrum,fb.T)
    ###MFCC = dct(np.log(mel_energy), norm='ortho', axis=0)
    feat = dct(np.log(mel_energy), norm='ortho')
    
    #feat: shape(#frame, #feature)
    #feat_dt: delta cepstrum
    #feat_ddt: delta-delta cepstrum
    feat_dt = np.concatenate((feat[None,1,:]-feat[None,0,:],
                              (feat[2:]-feat[:-2])/2,
                              feat[None,-1,:]-feat[None,-2,:]))
    feat_ddt = np.concatenate((feat_dt[None,1,:]-feat_dt[None,0,:],
                              (feat_dt[2:]-feat_dt[:-2])/2,
                              feat_dt[None,-1,:]-feat_dt[None,-2,:]))
    feat = feat+feat_dt/5+feat_ddt/10
    
    return feat[:,:13]
