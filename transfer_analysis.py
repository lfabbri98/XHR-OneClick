import classTransfer as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def extract_transfer_data(data: ct.Transfer, Cox, W, L, Total_dose, regime = "linear"):
    """
    Function that takes as input a data frame and returns another data frame containing the threshold voltage, mobility
    and subthreshold slope
    in function of time and dose. Data is a vector of objects Transfer
    """

    #Initialize threshold vector
    Vth = []
    Mu = []
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

    #Return subthreshold slope
    ss = extraction_subthreshold_slope(data)

    #Create the output dataframe
    output = {"Time": times, "Dose": dose, "Vth": Vth, "Mobility":Mu, "SS":ss }
    out = pd.DataFrame(output)
    return out

def extraction_subthreshold_slope(data: ct.Transfer):
    ss = []

    #First calculate the fitting range to find subthreshold slope
    #We can use the maximum slope as reference point and define a tolerance around it
    for i,j in enumerate(data):
        #Calculate first derivative
        vg = j.VG
        dvg = vg[1]-vg[0]
        id_prime = abs(np.gradient(j.ID, dvg))
        id2 = np.gradient(id_prime, dvg)
        max_id = np.argmax(id2)

        fig, ax = plt.subplots()
        ax.plot(vg, id2)
        plt.show()

        vg_low = vg[max_id - int(5/100 * max_id)]
        vg_high = vg[max_id + int(5/100 * max_id)]

        ss.append(j.calculate_subthreshold(vg_low, vg_high))
    
    return ss
