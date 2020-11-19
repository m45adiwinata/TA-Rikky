# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 16:24:17 2020

@author: m45ad
"""


import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
import os
import time
from statistics import mode

start_time = time.time()
#FUNGSI MFCC
def get_MFCC(sr,audio):
    #mfcc(signal, sample_rate, win_len, win_step, num_cep, ...) https:\\\\python-speech-features.readthedocs.io\\en\\latest\\
    features = mfcc.mfcc(audio, sr, 0.005, 0.01, 9, appendEnergy = False)      #PARAMETER MFCC DIATUR DISINI
    features = preprocessing.scale(features)        #PREPROCESSING FITUR DENGAN LIBRARY
    return features
#definisi filepath lagu asli / data model
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
    x = 0
    while(x < len(bits)):
        bitsx = bits[x:x+7*rates]                   #PENGAMBILAN PER 7 DETIK LAGU ASLI
        featurestemp2 = get_MFCC(rates, bitsx)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
        fitur_lagu_asli.append({'filepath': f, 'feature':featurestemp2})
        x += 7*rates                                #PERPINDAHAN INDEKS PENGAMBILAN LAGU ASLI
matched = []            #hasil pengenalan lagu asli terhadap lagu cover
matched_bool = []            #hasil pengenalan lagu asli terhadap lagu cover dalam bentuk Benar/Salah
idx_tests = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9}
#TENTUKAN DATASET TESTING
#test_set = np.append(filepath[0][:3], filepath[5][:3])
test_set = np.append(filepath[3][0], [])
#PERULANGAN PROSES PENGENALAN LAGU ASLI
for fi in test_set:
    matched_temp2 = [] #UNTUK MENAMPUNG MODUS MATCHED_TEMP KARENA 1 TEST_SET > 1 MODUS MATCHED_TEMP
    #MEMBACA DATA LAGU DARI FILEPATH.WAV
    rates0, bits0 = wavfile.read(fi)
    x = 0
    while(x < len(bits0)):
        bits0x = bits0[x:x+5*rates]                 #PENGAMBILAN PER 5 DETIK LAGU COVER
        featurestemp = get_MFCC(rates0, bits0x)     #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
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
            matched_temp.append(np.argmin(mean_ddws))    #MENCARI INDEX DDWS MINIMUM SEBAGAI HASIL PENGENALAN DAN DIKUMPULKAN KE ARRAY HASIL PENGENALAN
        #MENGUMPULKAN MODUS MATCHED_TEMP KE MATCHED_TEMP2
        if np.array(mode(matched_temp)).size > 1:
            for n in np.array(mode(matched_temp)):
                matched_temp2.append(n)
        else:
            matched_temp2.append(mode(matched_temp))
        x += 5 * rates0                             #PERPINDAHAN INDEKS PENGAMBILAN LAGU COVER
    #MENENTUKAN MATCHED_BOOL / BENAR ATAU SALAH
    if np.array(mode(matched_temp2)).size > 1:
        flag_benar = False
        temp = []
        for m in np.array(mode(matched_temp2)):
            matched.append(idx_tests[fitur_lagu_asli[m]['filepath'].split('\\')[-1].split('_')[0]])
            if idx_tests[fitur_lagu_asli[m]['filepath'].split('\\')[-1].split('_')[0]] == idx_tests[fi.split("\\")[2]]:
                matched_bool.append("Benar")
                flag_benar = True
        if flag_benar == False:
            matched_bool.append("Salah")
    else:
        matched.append(idx_tests[fitur_lagu_asli[mode(matched_temp2)]['filepath'].split('\\')[-1].split('_')[0]])
        if idx_tests[fitur_lagu_asli[mode(matched_temp2)]['filepath'].split('\\')[-1].split('_')[0]] == idx_tests[fi.split("\\")[2]]:
            matched_bool.append("Benar")
        else:
            matched_bool.append("Salah")
#MENGHITUNG WAKTU EKSEKUSI PROGRAM
seconds = time.time() - start_time
minutes = seconds // 60
seconds = seconds % 60
hours = minutes // 60
minutes = minutes % 60
print("--- Waktu eksekusi program: %s jam %s menit %.2f detik ---" % (hours, minutes, seconds))