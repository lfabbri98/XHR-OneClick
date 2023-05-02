"""
This file contains all the function to perform the import of the data from a folder and obtain transfer objects
"""

import classTransfer as ct
import pandas as pd
import numpy as np
import datetime as dt
import glob
import itertools

def read_file(path):
    #Function that reads a file from SMUCS and eventually separate it in subfiles if multiples acquisitions are contained.
    #Returns a vector of objects of class Transfer.
    names = ["VG","IG","tG","VD","ID","tD"]
    data = pd.read_csv(path, sep="\t", header=None, names = names)

    #Find lines where there is a string
    nan_list_o = []
    for i,j in enumerate(data.VG):
        try:
            float(j)
        except:
            nan_list_o.append(i)

    nan_list = [nan_list_o[i] for i in range(len(nan_list_o)) if i % 2 == 0]
    #print(nan_list)

    #Calculate VG length
    if len(nan_list)==1:
        VG_length = len(data.VG)-2
    else:
        VG_length = nan_list[1]-2

    transfers = []
    for j,k in enumerate(nan_list):
        #Time extraction
        t = data.tD[k][10:]
        dt_obj = dt.datetime.strptime(t, "%d/%m/%Y %H:%M:%S")

        #Data transfer extraction
        VG = np.array(data.VG[k+2:k+2+VG_length-1])
        VD = np.array(data.VD[k+2:k+2+VG_length-1])
        IG = np.array(data.IG[k+2:k+2+VG_length-1])
        ID = np.array(data.ID[k+2:k+2+VG_length-1])

        for i in range(len(VG)):
            VG[i] = float(VG[i])
            VD[i] = float(VD[i])
            IG[i] = float(IG[i])
            ID[i] = float(ID[i])
            

        obj = ct.Transfer(VG, IG, VD, ID, dt_obj)
        transfers.append(obj)
    #if len(nan_list)>1:
        #transfers[0].time = transfers[1].time-dt.timedelta(seconds=40)
        
    return transfers

def read_folder(path):
    files = []
    file_list = glob.glob(path)

    for i in range(len(file_list)):
        file = read_file(file_list[i])
        files.append(file)

    #make the file list flat
    files = list(itertools.chain(*files))
    
    #Order the files according to date
    files_sorted = sorted(files, key=lambda x: x.time)

    return files_sorted

    