import classTransfer as ct
import numpy as np
import pandas as pd

def extract_transfer_data(data: ct.Transfer, Cox, W, L, Total_dose, regime = "linear"):
    """
    Function that takes as input a data frame and returns another data frame containing the threshold voltage, mobility
    and subthreshold slope
    in function of time and dose. Data is a vector of objects Transfer
    """

    #Initialize threshold vector
    Vth = []
    Mu = []
    ss = []
    times = []

    #Determine ID threshold for mobility and threshold voltage.
    ID_min = np.inf
    for i,j in enumerate(data):
        if max(j.ID)<ID_min:
            ID_min = max(j.ID)
        else:
            continue
    
    #Consider a tolerance between the minimum to obtain the linear fit, like 10%
    ID_min_select = ID_min - (ID_min *10/100)


    #Use the limit values to fit every curve
    for i,j in enumerate(data):
        Vth.append(j.calculate_threshold(ID_min_select))
        Mu.append(j.calculate_mobility(ID_min_select, Cox, W, L, regime))
        times.append(j.time-data[0].time) #Relative time from beginning of measure
    
    #Calculate dose array
    dose = np.linspace(0,Total_dose, len(Vth))

    #Create the output dataframe
    output = {"Time": times, "Dose": dose, "Vth": Vth, "Mobility":Mu }
    out = pd.DataFrame(output)
    return out

