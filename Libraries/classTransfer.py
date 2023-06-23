import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
import configparser

def poly1(x,a,b):
    return a*x + b

class Transfer:

    #Attributes
    VG = [] #Gate voltage
    IG = [] #Gate current
    VD = [] #Drain voltage
    ID = [] #Drain current
    time = 0

    #Functions
    def __init__(self, VG_init, IG_init, VD_init, ID_init, time):
        self.VG = VG_init
        self.ID = abs(ID_init)
        self.IG = IG_init
        self.VD = VD_init
        self.time = time

    #Function to calculate the threshold voltage
    def calculate_threshold(self, ID_threshold, select="linear"):
        if select == "linear":
            mask = np.where(self.ID>ID_threshold)[0]
            popt, pcov = curve_fit(poly1, self.VG[mask], self.ID[mask])
            return(-popt[1]/popt[0])
        elif select=="saturation":
            ID_sqrt = np.sqrt(self.ID)
            mask = np.where(ID_sqrt>ID_threshold)[0]
            popt, pcov = curve_fit(poly1, self.VG[mask], ID_sqrt[mask])
            return(-popt[1]/popt[0])
        
        return 0
    
    def calculate_mobility(self, ID_threshold, Cox, W, L,N, select="linear"):
        if select == "linear":
            mask = np.where(self.ID>ID_threshold)[0]
            popt, pcov = curve_fit(poly1, self.VG[mask], self.ID[mask])
            return(popt[0]*L/(W*Cox*self.VD[1]*N))
        if select == "saturation":
            ID_sqrt = np.sqrt(self.ID)
            mask = np.where(ID_sqrt>ID_threshold)[0]
            popt, pcov = curve_fit(poly1, self.VG[mask], ID_sqrt[mask])
            return(popt[0]*L*2/(W*Cox*N))
        
        return 0
    
    def calculate_subthreshold(self, min_index, max_index):
        ID_log = []
        for k,l in enumerate(self.ID):
            try:
                a = np.log10(self.ID[k])
            except:
                a=np.log10(self.ID[k-1])
               
            ID_log.append(a)
        
        
        try:
            popt, pcov = curve_fit(poly1, self.VG[min_index:max_index], ID_log[min_index:max_index])
            von = (-11-popt[1])/popt[0]
            if von<min(self.VG): print("Von out of measure range!")
            return 1/popt[0] , von

        except:
            return float('NaN'), float('NaN')


    #Function to plot transfer in log and lin scale
    def plot_transfer(self):
        fig, ax = plt.subplots()
        ax.plot(self.VG, self.ID)
        ax.set_xlabel("$V_G$ (V)")
        ax.set_ylabel("$I_D$ (A)")

        fig2, ax2 = plt.subplots()
        ax2.plot(self.VG, self.ID)
        ax2.set_yscale("log")
        ax2.set_xlabel("$V_G$ (V)")
        ax2.set_ylabel("$I_D$ (A)")

        plt.show()

def import_parameters(config_path):
    """
    Function to call config parser and acquire paths and parameters from the configuration file.

    Returns the important parameters of the program.
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    irrad_path = config.get("settings", "irradiation_folder_path" )
    rec_path = config.get("settings", "recovery_folder_path" )
    Cox = config.get("settings","cox")
    W = config.get("settings","W")
    L = config.get("settings","L")
    Total_dose = config.get("settings","Total_dose")
    N = config.get("settings","NumberDevicesInArray")
    Ntrans = config.get("Output", "MaximumNumberTransfer")

    outputpath = config.get("output", "Output_Path")

    Cox = float(Cox)
    W = float(W)
    L = float(L)
    Total_dose = float(Total_dose)
    N = float(N)
    Ntrans = float()

    return irrad_path, rec_path, Cox, W, L,Total_dose, outputpath, N, Ntrans
        

def read_recovery_fit(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    use_custom = config.get("recovery", "UseCustomInitialParameters")
    Vth0 = config.get("recovery","vth_perm")
    alpha = config.get("recovery","alpha")
    gamma = config.get("recovery","gamma")

    return use_custom, [float(alpha), float(gamma), float(Vth0)]
