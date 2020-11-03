# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 19:02:16 2020

@author: m45ad
"""


import scipy.io.wavfile as wavfile
import python_speech_features as mfcc
from sklearn import preprocessing
import os
import matplotlib.pyplot as plt

def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https://python-speech-features.readthedocs.io/en/latest/
    features = mfcc.mfcc(audio, sr, 0.025, 0.025, 20, appendEnergy = False)
    features = preprocessing.scale(features)
    return features

path_asli = '..\\Data Lagu\\asli\\reff'
filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]

#PENGUMPULAN FITUR DARI FILE LAGU ASLI
fitur_lagu_asli = []
for f in filepath_asli:
    rates, bits = wavfile.read(f)
    featurestemp2 = get_MFCC(rates, bits)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
    fitur_lagu_asli.append({'filepath': f, 'feature':featurestemp2})

plt.plot(fitur_lagu_asli[0]['feature'])