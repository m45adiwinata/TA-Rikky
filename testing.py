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

#FUNGSI MFCC
def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https:\\\\python-speech-features.readthedocs.io\\en\\latest\\
    features = mfcc.mfcc(audio, sr, 0.009, 0.01, 9, appendEnergy = False)      #PARAMETER MFCC DIATUR DISINI
    features = preprocessing.scale(features)        #PREPROCESSING FITUR DENGAN LIBRARY
    return features
#definisi filepath lagu asli / data model
path_asli = '..\\Data Lagu\\asli\\reff'
filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
#definisi filepath lagu cover / data testing
path = [
        '..\\Data Lagu\\1\\reff - 16000',
        '..\\Data Lagu\\2\\reff - 16000',
        '..\\Data Lagu\\3\\reff - 16000',
        '..\\Data Lagu\\4\\reff - 16000',
        '..\\Data Lagu\\5\\reff - 16000',
        '..\\Data Lagu\\6\\reff - 16000',
        '..\\Data Lagu\\7\\reff - 16000',
        '..\\Data Lagu\\8\\reff - 16000',
        '..\\Data Lagu\\9\\reff - 16000',
        '..\\Data Lagu\\10\\reff - 16000'
        ]
filepath = []
for p in path:
    filepath.append([os.path.join(p,fname) for fname in os.listdir(p) if fname.endswith('.wav')])

matched = []            #hasil pengenalan lagu asli terhadap lagu cover
#TENTUKAN DATASET TESTING
#test_set = np.append(filepath[0][:3], filepath[5][:3])
test_set = np.append(filepath[8][3], [])
#PERULANGAN PROSES PENGENALAN LAGU ASLI
for fi in test_set:
    rates0, bits0 = wavfile.read(fi)        #BACA SAMPLING RATES DAN BIT DATA LAGU COVER
    features0 = get_MFCC(rates0, bits0)     #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
    y = []
    #MENGUBAH FITUR KE FITUR VEKTOR
    for f in features0:
        y.append(np.sum(f))
    y = np.array(y)     #FITUR VEKTOR LAGU COVER SUDAH SIAP
    
    mean_ddws = []
    #PERULANGAN UNTUK PROSES DTW FITUR LAGU COVER DENGAN FITUR LAGU ASLI
    for f in filepath_asli:    
        rates, bits = wavfile.read(f)       #BACA SAMPLING RATES DAN BIT DATA LAGU ASLI
        features = get_MFCC(rates, bits)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
        x = []
        #MENGUBAH FITUR KE FITUR VEKTOR
        for f in features:
            x.append(np.sum(f))
        x = np.array(x)
        d = np.zeros((y.size, x.size), dtype=int)
        #PERULANGAN UNTUK PROSES DTW
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
        #PERULANGAN UNTUK MENGHITUNG JARAK SETIAP STEP DTW
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
        mean_ddws.append(np.mean(ddw))      #MENGUMPULKAN HASIL RATA-RATA JARAK SETIAP STEP DTW (DDWS)
    matched.append(np.argmin(mean_ddws))    #MENCARI INDEX DDWS MINIMUM SEBAGAI HASIL PENGENALAN DAN DIKUMPULKAN KE ARRAY HASIL PENGENALAN