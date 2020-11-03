# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 21:45:01 2020

@author: MAY
"""

import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
import os

def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https://python-speech-features.readthedocs.io/en/latest/
    features = mfcc.mfcc(audio, sr, 0.025, 0.025, 20, appendEnergy = False)
    features = preprocessing.scale(features)
    return features

path_asli = '..\\Data Lagu\\asli\\reff'
filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
#definisi filepath lagu cover / data testing
path = [
        '..\\Data Lagu\\01\\reff',
        '..\\Data Lagu\\02\\reff',
        '..\\Data Lagu\\03\\reff',
        '..\\Data Lagu\\04\\reff',
        '..\\Data Lagu\\05\\reff',
        '..\\Data Lagu\\06\\reff',
        '..\\Data Lagu\\07\\reff',
        '..\\Data Lagu\\08\\reff',
        '..\\Data Lagu\\09\\reff',
        '..\\Data Lagu\\10\\reff'
        ]
filepath = []
for p in path:
    filepath.append([os.path.join(p,fname) for fname in os.listdir(p) if fname.endswith('.wav')])

#PENGUMPULAN FITUR DARI FILE LAGU ASLI
fitur_lagu_asli = []
for f in filepath_asli:
    rates, bits = wavfile.read(f)
    featurestemp2 = get_MFCC(rates, bits)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
    fitur_lagu_asli.append({'filepath': f, 'feature':featurestemp2})
fi = filepath[0][0]
rates0, bits0 = wavfile.read(fi)
featurestemp = get_MFCC(rates0, bits0)     #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
matched_temp = []
for fb in range(featurestemp.shape[1]):
    features0 = featurestemp[:,fb]
    mean_ddws = []
    for f in fitur_lagu_asli:
        print("Pencocokkan dengan lagu " + f['filepath'].split('\\')[-1].split('.')[0])
        featurestemp2 = f['feature']
        features = featurestemp2[:, fb]
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
    
x = np.array(w)     #SILAHKAN DI PLOT