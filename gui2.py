# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:13:54 2020

@author: m45ad
"""


import scipy.io.wavfile as wavfile
import numpy as np
import python_speech_features as mfcc
from sklearn import preprocessing
import os
from statistics import mode
from tkinter import Tk, Frame, Text, Label, Button, Entry, StringVar, Canvas, Scrollbar
from tkinter import ttk
from tkinter import filedialog

class App(Tk):
    def __init__(self,*args,**kwargs):
       Tk.__init__(self,*args,**kwargs)
       self.notebook = ttk.Notebook()
       self.add_tab()
       self.notebook.grid(row=0)
  
    def add_tab(self):
        tab1 = identify(self.notebook)
        tab3 = testing(self.notebook)
        self.notebook.add(tab1,text="Identifikasi Cover")
        self.notebook.add(tab3,text="Pengujian Sistem")
        
class identify(Frame):
    def __init__(self,name,*args,**kwargs):        
        Frame.__init__(self,*args,**kwargs)
        self.TextData = Text(self)
        self.LabelData = Label(self)
        path_asli = '..\\Data Lagu\\asli\\reff'
        self.filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
        self.idx_tests = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9}
        lblInputLagu = Label(self, text="Input Lagu")
        lblInputLagu.grid(row=0, column=0)
        lblLagu = Label(self, text="Lagu")
        lblLagu.grid(row=1, column=0)
        self.lblFilepath = Label(self, text="...", width="40", background="white")
        self.lblFilepath.grid(row=1, column=1, pady=10, columnspan=3, sticky="W")
        self.BtnBrowse = Button(self, text="Pilih", command=self.fileDialog)
        self.BtnBrowse.grid(row=1, column=4, pady=10, padx=10, sticky="E")
        self.btnReset = Button(self, text="Reset", command=self.reset)
        self.btnReset.grid(row=1, column=5)
        lblFbank = Label(self, text="Filter Bank")
        lblFbank.grid(row=2, column=0, padx=5, pady=10, sticky="E")
        self.fbank = StringVar(value="20")
        entFbank = Entry(self, textvariable=self.fbank)
        entFbank.grid(row=2, column=1, sticky="W", pady=10)
        lblWinlen = Label(self, text="WinLen")
        lblWinlen.grid(row=2, column=2, sticky="E")
        self.winlen = StringVar(value="0.05")
        entWinlen = Entry(self, textvariable=self.winlen)
        entWinlen.grid(row=2, column=3, sticky="W", pady=10)
        lblWinstep = Label(self, text="WinStep")
        lblWinstep.grid(row=2, column=4, sticky="E")
        self.winstep = StringVar(value="0.025")
        entWinstep = Entry(self, textvariable=self.winstep)
        entWinstep.grid(row=2, column=5, sticky="W", pady=10)
        self.BtnIdentifying = Button(self, text="Identifikasi", pady=5, padx=10, command=self.identifikasi)
        self.BtnIdentifying.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="E")
        lblIdentLagu = Label(self, text="Identifikasi Lagu")
        lblIdentLagu.grid(row=4, column=0, padx=5)
        lblHasil = Label(self, text="Hasil")
        lblHasil.grid(row=5, column=0)
        self.hCover = StringVar(value="")
        entHasilCover = Entry(self, textvariable=self.hCover)
        entHasilCover.grid(row=5, column=1, sticky="E")
        lblEqual = Label(self, text="=")
        lblEqual.grid(row=5, column=2)
        self.hAsli = StringVar(value="")
        entHasilAsli = Entry(self, textvariable=self.hAsli)
        entHasilAsli.grid(row=5, column=3)
        self.kesimpulan = StringVar(value="")
        entKesimpulan = Entry(self, textvariable=self.kesimpulan)
        entKesimpulan.grid(row=6, column=0, padx=10, pady=5)
        
    def fileDialog(self):
        filepath = filedialog.askopenfilename(initialdir = "../", title = "select a file", filetype = (("Wave", "*.wav"), ("All Files", "*.*")))
        if len(filepath) > 0:
            self.folderpath = filepath.split('/')[-3]
            temp = '.../' + ('/').join(filepath.split('/')[-3:])
            self.lblFilepath.config(text=temp)
            self.filepath = filepath
            
    def get_MFCC(self, sr,audio):
        features = mfcc.mfcc(audio, sr, float(self.winlen.get()), float(self.winstep.get()), int(self.fbank.get()), appendEnergy = False)
        features = preprocessing.scale(features)
        return features
    
    def reset(self):
        self.filepath = None
        self.lblFilepath.config(text="...")
        self.hCover.set("")
        self.hAsli.set("")
        self.kesimpulan.set("")
    
    def identifikasi(self):
        self.fitur_lagu_asli = []
        for f in self.filepath_asli:
            rates, bits = wavfile.read(f)
            x = 0
            while(x < len(bits)):
                bitsx = bits[x:x+7*rates]                   #PENGAMBILAN PER 7 DETIK LAGU ASLI
                featurestemp2 = self.get_MFCC(rates, bitsx)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
                self.fitur_lagu_asli.append({'filepath': f, 'feature':featurestemp2})
                x += 7*rates                                #PERPINDAHAN INDEKS PENGAMBILAN LAGU ASLI
        matched = []
        matched_bool = []
        test_set = np.array([self.filepath])
        for fi in test_set:
            matched_temp2 = [] #UNTUK MENAMPUNG MODUS MATCHED_TEMP KARENA 1 TEST_SET > 1 MODUS MATCHED_TEMP
            rates0, bits0 = wavfile.read(fi)
            x = 0
            while(x < len(bits0)):
                bits0x = bits0[x:x+5*rates]                 #PENGAMBILAN PER 5 DETIK LAGU COVER
                featurestemp = self.get_MFCC(rates0, bits0x)
                matched_temp = []
                matched_temp_val = []
                for fb in range(featurestemp.shape[1]):
                    features0 = featurestemp[:,fb]
                    mean_ddws = []
                    for f in self.fitur_lagu_asli:
                        print("Pencocokkan dengan lagu " + f['filepath'].split('\\')[-1].split('.')[0])
                        featurestemp2 = f['feature']
                        features = featurestemp2[:, fb]
                        i = 0
                        j = 0
                        w = []
                        dw = []
                        while i < len(features0) or j < len(features):
                            dw.append(np.abs(features0[i] - features[j]))
                            w.append([i, j])
                            if i == len(features0)-1 and j < len(features)-1:
                                j += 1
                            elif j == len(features)-1 and i < len(features0)-1:
                                i += 1
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
                        for i in range(len(dw) - 1):
                            ddw.append(np.abs(dw[i+1] - dw[i]))
                        mean_ddws.append(np.mean(ddw))
                    matched_temp.append(np.argmin(mean_ddws))
                    matched_temp_val.append(min(mean_ddws))
                if np.array(mode(matched_temp)).size > 1:
                    for n in np.array(mode(matched_temp)):
                        matched_temp2.append(n)
                else:
                    matched_temp2.append(mode(matched_temp))
                x += 5 * rates0                             #PERPINDAHAN INDEKS PENGAMBILAN LAGU COVER
            #MENENTUKAN MATCHED_BOOL / BENAR ATAU SALAH
            if np.array(mode(matched_temp2)).size > 1:
                temp = []
                temp_bool = []
                for m in np.array(mode(matched_temp2)):
                    idx_terdeteksi = self.idx_tests[self.fitur_lagu_asli[m]['filepath'].split('\\')[-1].split('_')[0]]
                    temp.append(idx_terdeteksi)
                    print(fi)
                    if idx_terdeteksi == self.idx_tests[fi.split("/")[-3]]:
                        temp_bool.append("Benar")
                    else:
                        temp_bool.append("Salah")
                matched.append(temp)
                if np.array(mode(temp_bool)).size > 1:
                    matched_bool.append("Benar")
                    matched_choosen = self.folderpath
                elif mode(temp_bool) == "Benar":
                    matched_bool.append("Benar")
                    matched_choosen = self.folderpath
                else:
                    matched_bool.append("Salah")
                    matched_choosen = self.fitur_lagu_asli[matched_temp[np.argmin(matched_temp_val)]]['filepath'].split('\\')[-1].split('_')[0]
            else:
                idx_terdeteksi = self.idx_tests[self.fitur_lagu_asli[mode(matched_temp2)]['filepath'].split('\\')[-1].split('_')[0]]
                matched.append(idx_terdeteksi)
                print(fi)
                if idx_terdeteksi == self.idx_tests[fi.split("/")[-3]]:
                    matched_bool.append("Benar")
                    matched_choosen = self.folderpath
                else:
                    matched_bool.append("Salah")
                    matched_choosen = self.fitur_lagu_asli[matched_temp[np.argmin(matched_temp_val)]]['filepath'].split('\\')[-1].split('_')[0]
        self.hCover.set(self.folderpath)
        self.hAsli.set(matched_choosen)
        self.kesimpulan.set(matched_bool[0])
    
class testing(Frame):
    def __init__(self,name,*args,**kwargs):
        Frame.__init__(self,*args,**kwargs)
        self.TextTraining = Text(self)
        path_asli = '..\\Data Lagu\\asli\\reff'
        self.filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
        self.idx_tests = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9}
        lblTop = Label(self, text="Pengujian Data Uji")
        lblTop.grid(row=0, column=0)
        lblFbank = Label(self, text="Filter Bank")
        lblFbank.grid(row=1, column=0, padx=5, pady=10, sticky="E")
        self.fbank = StringVar(value="20")
        entFbank = Entry(self, textvariable=self.fbank)
        entFbank.grid(row=1, column=1, sticky="W", pady=10)
        lblWinlen = Label(self, text="WinLen")
        lblWinlen.grid(row=1, column=2, sticky="E")
        self.winlen = StringVar(value="0.05")
        entWinlen = Entry(self, textvariable=self.winlen)
        entWinlen.grid(row=1, column=3, sticky="W", pady=10)
        lblWinstep = Label(self, text="WinStep")
        lblWinstep.grid(row=1, column=4, sticky="E")
        self.winstep = StringVar(value="0.025")
        entWinstep = Entry(self, textvariable=self.winstep)
        entWinstep.grid(row=1, column=5, sticky="W", pady=10)
        btnUji = Button(self, text="Uji", command=self.testing)
        btnUji.grid(row=2, column=3)
        btnReset = Button(self, text="Reset", command=self.reset)
        btnReset.grid(row=2, column=5)
        lblHasil = Label(self, text="Hasil Pengujian")
        lblHasil.grid(row=3, column=0)
        self.frmTabelHasil = Frame(self)
        self.frmTabelHasil.grid(row=4, column=0, columnspan=6)
        self.scrollFrame = ScrollFrame(self.frmTabelHasil)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        lblLaguAsli = Label(self.scrollFrame.viewPort, text="Lagu Asli", width="20")
        lblLaguAsli.grid(row=0, column=0)
        lblBatasTabel = Label(self.scrollFrame.viewPort, text="|")
        lblBatasTabel.grid(row=0, column=1)
        lblHasilUji = Label(self.scrollFrame.viewPort, text="Hasil", width="20")
        lblHasilUji.grid(row=0, column=2)
        lblAkurasi = Label(self, text="Akurasi")
        lblAkurasi.grid(row=5, column=0, padx=10, pady=10)
        lblEqual = Label(self, text="=")
        lblEqual.grid(row=5, column=1)
        self.akurasi = StringVar(value="")
        entAkurasi = Entry(self, textvariable=self.akurasi)
        entAkurasi.grid(row=5, column=2)
        
    def get_MFCC(self, sr,audio):
        features = mfcc.mfcc(audio, sr, float(self.winlen.get()), float(self.winstep.get()), int(self.fbank.get()), appendEnergy = False)
        features = preprocessing.scale(features)
        return features
    
    def reset(self):
        self.scrollFrame.destroy()
        self.scrollFrame = ScrollFrame(self.frmTabelHasil)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
        lblLaguAsli = Label(self.scrollFrame.viewPort, text="Lagu Asli", width="20")
        lblLaguAsli.grid(row=0, column=0)
        lblBatasTabel = Label(self.scrollFrame.viewPort, text="|")
        lblBatasTabel.grid(row=0, column=1)
        lblHasilUji = Label(self.scrollFrame.viewPort, text="Hasil", width="20")
        lblHasilUji.grid(row=0, column=2)
        self.akurasi.set("")
    
    def testing(self):
        path_asli = '..\\Data Lagu\\asli\\reff'
        filepath_asli = [os.path.join(path_asli,fname) for fname in os.listdir(path_asli) if fname.endswith('.wav')]
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
        fitur_lagu_asli = []
        for f in filepath_asli:
            rates, bits = wavfile.read(f)
            x = 0
            while(x < len(bits)):
                bitsx = bits[x:x+7*rates]                   #PENGAMBILAN PER 7 DETIK LAGU ASLI
                featurestemp2 = self.get_MFCC(rates, bitsx)    #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
                fitur_lagu_asli.append({'filepath': f, 'feature':featurestemp2})
                x += 7*rates                                #PERPINDAHAN INDEKS PENGAMBILAN LAGU ASLI
        matched = []            #hasil pengenalan lagu asli terhadap lagu cover
        matched_bool = []            #hasil pengenalan lagu asli terhadap lagu cover dalam bentuk Benar/Salah
        matched_bool_sums = []
        idx_tests = {'01':0, '02':1, '03':2, '04':3, '05':4, '06':5, '07':6, '08':7, '09':8, '10':9}
        for test_set in filepath:
            matched_bool_int = []
            for fi in test_set:
                rates0, bits0 = wavfile.read(fi)
                x = 0
                while(x < len(bits0)):
                    bits0x = bits0[x:x+5*rates]                 #PENGAMBILAN PER 5 DETIK LAGU COVER
                    featurestemp = self.get_MFCC(rates0, bits0x)     #EKSTRAKSI FITUR DENGAN MEMANGGIL FUNGSI MFCC
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
                    matched.append(mode(matched_temp))
                    if np.array(mode(matched_temp)).size > 1:
                        flag_benar = False
                        for m in np.array(mode(matched_temp)):
                            idx_terdeteksi = fitur_lagu_asli[m]['filepath'].split("\\")[-1].split("_")[0]
                            if idx_terdeteksi == fi.split("\\")[-3]:
                                matched_bool.append("Benar")
                                matched_bool_int.append(1)
                                flag_benar = True
                        if flag_benar == False:
                            matched_bool.append("Salah")
                            matched_bool_int.append(0)
                    else:
                        idx_terdeteksi = fitur_lagu_asli[mode(matched_temp)]['filepath'].split("\\")[-1].split("_")[0]
                        if idx_terdeteksi == idx_tests[fi.split("\\")[-3]]:
                            matched_bool.append("Benar")
                            matched_bool_int.append(1)
                        else:
                            matched_bool.append("Salah")
                            matched_bool_int.append(0)
                    x += 5*rates0                             #PERPINDAHAN INDEKS PENGAMBILAN LAGU COVER
            lblTemp = Label(self.scrollFrame.viewPort, text=test_set[0].split('\\')[-3])
            lblTemp.grid(row=int(test_set[0].split('\\')[-3]), column=0)
            lblBatasTabel = Label(self.scrollFrame.viewPort, text="|")
            lblBatasTabel.grid(row=int(test_set[0].split('\\')[-3]), column=1)
            lblTemp = Label(self.scrollFrame.viewPort, text=str(np.sum(matched_bool_int)))
            lblTemp.grid(row=int(test_set[0].split('\\')[-3]), column=2)
            matched_bool_sums.append(np.sum(matched_bool_int))
        self.akurasi.set(str(np.sum(matched_bool_sums)) + '%')
        
class ScrollFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)
        self.canvas = Canvas(self, borderwidth=0)          #place canvas on self
        self.viewPort = Frame(self.canvas)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")
        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.

my_app = App()
my_app.title("Identifikasi Cover Lagu")
# my_app.geometry('1366x768')
# my_app.state('zoomed')
my_app.mainloop()