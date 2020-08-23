# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:33:16 2020

@author: m45ad
"""


import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
import os

def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https:\\\\python-speech-features.readthedocs.io\\en\\latest\\
    features = mfcc.mfcc(audio, sr, 0.05, 0.025, 20, appendEnergy = False)
    features = preprocessing.scale(features)
    return features

path_asli = 'Data Lagu\\asli\\awal-reff'
filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]

path = [
        'Data Lagu\\1\\awal-reff - 16000',
        'Data Lagu\\2\\awal-reff - 16000',
        'Data Lagu\\3\\awal-reff - 16000',
        'Data Lagu\\4\\awal-reff - 16000',
        'Data Lagu\\5\\awal-reff - 16000',
        'Data Lagu\\6\\awal-reff - 16000',
        'Data Lagu\\7\\awal-reff - 16000',
        'Data Lagu\\8\\awal-reff - 16000',
        'Data Lagu\\9\\awal-reff - 16000',
        'Data Lagu\\10\\awal-reff - 16000'
        ]
filepath = []
for p in path:
    filepath.append([os.path.join(p,fname) for fname in os.listdir(p) if fname.endswith('.wav')])

matched = []
#test_set = np.append(filepath[0][:3], filepath[5][:3])
test_set = np.append(filepath[5][:3], [])
for fi in test_set:
    rates0, bits0 = wavfile.read(fi)
    features0 = get_MFCC(rates0, bits0)
    y = []
    for f in features0:
        y.append(np.sum(f))
    y = np.array(y)
    
    mean_ddws = []
    for f in filepath_asli:    
        rates, bits = wavfile.read(f)
        features = get_MFCC(rates, bits)
        x = []
        for f in features:
            x.append(np.sum(f))
        x = np.array(x)
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
        mean_ddws.append(np.mean(ddw))
    matched.append(np.argmin(mean_ddws))