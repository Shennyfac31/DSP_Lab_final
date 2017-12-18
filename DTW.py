# -*- coding: utf-8 -*-
"""
Final project

DTW function
"""

import numpy as np

#DTW
def DTW(s1,s2):
    '''
    s1, s2: MFCC features of frames, 2D, shape: (frame_num, feat_num)
    '''
    m = len(s1)
    n = len(s2)
    D = np.sum(np.abs(s1[:,:,None]-s2[:,:,None].T),axis=1)
    
    #find accumulated cost matrix D
    for i in range(1,m):
        D[i,0] = D[i-1,0] + D[i,0]
    for j in range(1,n):
        D[0,j] = D[0,j-1] + D[0,j]
    for i in range(1,m):
        for j in range(1,n):
            D[i,j] = D[i,j] + min(D[i-1,j],D[i-1,j-1],D[i,j-1])
    
    return D[-1,-1]
