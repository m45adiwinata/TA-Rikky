# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 09:55:01 2020

@author: m45ad
"""


import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
import os
import time

start_time = time.time()
#FUNGSI MFCC
def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https:\\\\python-speech-features.readthedocs.io\\en\\latest\\
    features = mfcc.mfcc(audio, sr, 0.05, 0.025, 20, appendEnergy = False)      #PARAMETER MFCC DIATUR DISINI
    features = preprocessing.scale(features)        #PREPROCESSING FITUR DENGAN LIBRARY
    return features
#definisi filepath lagu asli / data model
path_asli = '..\\Data Lagu\\asli\\reff'
filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
#definisi filepath lagu cover / data testing
path = [
        '..\\Data Lagu\\1\\reff',
        '..\\Data Lagu\\2\\reff',
        '..\\Data Lagu\\3\\reff',
        '..\\Data Lagu\\4\\reff',
        '..\\Data Lagu\\5\\reff',
        '..\\Data Lagu\\6\\reff',
        '..\\Data Lagu\\7\\reff',
        '..\\Data Lagu\\8\\reff',
        '..\\Data Lagu\\9\\reff',
        '..\\Data Lagu\\10\\reff'
        ]
filepath = []
for p in path:
    filepath.append([os.path.join(p,fname) for fname in os.listdir(p) if fname.endswith('.wav')])

matched = []            #hasil pengenalan lagu asli terhadap lagu cover
#TENTUKAN DATASET TESTING
#test_set = np.append(filepath[0][:3], filepath[5][:3])
test_set = np.append(filepath[0][2], [])
#PERULANGAN PROSES PENGENALAN LAGU ASLI
for fi in test_set:
    #MEMBACA DATA LAGU DARI FILEPATH.WAV
    rates0, bits0 = wavfile.read(fi)
    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
    featurestemp = get_MFCC(rates0, bits0)
    features0 = []
    #PENJUMLAHAN MASING-MASING FILTER BANK UNTUK MEMBUAT FITUR VEKTOR
    for y in featurestemp:
        features0.append(np.sum(y))
    features0 = np.array(features0)
    mean_ddws = []
    #PERULANGAN UNTUK MENCOCOKKAN DENGAN LAGU ASLI
    for f in filepath_asli:
        print("Pencocokkan dengan lagu " + f.split('\\')[-1].split('.')[0])
        rates, bits = wavfile.read(f)
        featurestemp2 = get_MFCC(rates, bits)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
        features = []
        for x in featurestemp2:
            features.append(np.sum(x))
        features = np.array(features)
        i = 0
        j = 0
        w = []
        dw = []
        #i <= JML FITUR LAGU COVER, j <= JML FITUR LAGU ASLI
        while i < len(features0) or j < len(features):
            dw.append(np.abs(features0[i] - features[j]))
            w.append([i, j])
            #JIKA i SUDAH MENTOK DAN j BELUM MENTOK, MAKA DTW AKAN DILANJUTKAN KE ARAH [j+1]
            if i == len(features0)-1 and j < len(features)-1:
                j += 1
            #JIKA j SUDAH MENTOK DAN i BELUM MENTOK, MAKA DTW AKAN DILANJUTKAN KE ARAH [i+1]
            elif j == len(features)-1 and i < len(features0)-1:
                i += 1
            #JIKA i DAN j SAMA" TIDAK MENTOK, MAKA DICARI DULU HASIL MINIMUM [i+1], [i+1, j+1], [j+1] UNTUK MENJADI ARAH DTW
            elif i < len(features0)-1 and j < len(features)-1:
                d = []
                d.append(np.abs(features0[i+1] - features[j]))
                d.append(np.abs(features0[i+1] - features[j+1]))
                d.append(np.abs(features0[i] - features[j+1]))
                if np.argmin(d) == 0:
                    i += 1
                elif np.argmin(d) == 1:
                    i += 1
                    j += 1
                else:
                    j += 1
            elif i == len(features0)-1 and j == len(features)-1:
                i += 1
                j += 1
            
        ddw = []
        i = 0
        #MENGHITUNG PANJANG SETIAP LANGKAH DTW
        for i in range(len(dw) - 1):
            ddw.append(np.abs(dw[i+1] - dw[i]))
        mean_ddws.append(np.mean(ddw))      #MENGUMPULKAN HASIL RATA-RATA JARAK SETIAP STEP DTW (DDWS)
    matched.append(np.argmin(mean_ddws))    #MENCARI INDEX DDWS MINIMUM SEBAGAI HASIL PENGENALAN DAN DIKUMPULKAN KE ARRAY HASIL PENGENALAN
#MENGHITUNG WAKTU EKSEKUSI PROGRAM
seconds = time.time() - start_time
minutes = seconds // 60
seconds = seconds % 60
hours = minutes // 60
minutes = minutes % 60
print("--- Waktu eksekusi program: %s jam %s menit %.2f detik ---" % (hours, minutes, seconds))