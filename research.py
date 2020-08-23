# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:45:01 2020

@author: MAY
"""

import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing

def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https://python-speech-features.readthedocs.io/en/latest/
    features = mfcc.mfcc(audio, sr, 0.025, 0.025, 20, appendEnergy = False)
    features = preprocessing.scale(features)
    return features

rates, bits = wavfile.read("awal-reff.wav")
features = get_MFCC(rates, bits)
x = []
for f in features:
    x.append(np.sum(f))
x = np.array(x)

rates0, bits0 = wavfile.read("awal-reff asli.wav")
features0 = get_MFCC(rates0, bits0)
y = []
for f in features0:
    y.append(np.sum(f))
y = np.array(y)

d = np.zeros((y.size, x.size), dtype=int)
for i in range(len(y)):
    for j in range(len(x)):
        if i % 100 == 0 and j == 0:
            print("Progress: %d/%d" % (i, len(y)))
        if i == 0 and j == 0:
            d[i,j] = np.abs(y[i] - x[j])
        elif i == 0:
            d[i,j] = np.abs(y[i] - x[j]) + d[0, j-1]
        elif j == 0:
            d[i,j] = np.abs(y[i] - x[j]) + d[i-1, 0]
        else:
            d[i,j] = np.abs(y[i] - x[j]) + np.min([d[i-1, j-1], d[i, j-1], d[i-1, j]])

w = []
dw = []
i=0
j=0
while i < d.shape[0]-1 and j < d.shape[1]-1:
    w.append([i, j])
    dw.append(d[i,j])
    temp = np.argmin([d[i+1, j], d[i+1, j+1], d[i, j+1]])
    if i < d.shape[0] - 1 and j < d.shape[1] - 1:
        if temp == 0:
            i+=1
        elif temp == 1:
            i+=1
            j+=1
        else:
            j+=1
    elif j == d.shape[1] - 1:
        i+=1
    elif i == d.shape[0] - 1:
        j+=1
    
ddw = []
for i in range(len(dw) - 1):
    ddw.append(dw[i+1] - dw[i])