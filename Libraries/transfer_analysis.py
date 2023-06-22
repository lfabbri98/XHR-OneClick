import Libraries.classTransfer as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import datetime

#------------------------
# Support functions
#------------------------

def derivative(vector):
    """
    Calculates the derivative function of a vector.
    
    Arguments:
    vector -- a list or NumPy array representing the vector
    
    Returns:
    derivative -- a list or NumPy array representing the derivative of the vector
    """
    
    # Calculate the differences between adjacent elements of the vector
    diffs = [vector[i+1] - vector[i] for i in range(len(vector)-1)]
    
    # Calculate the average difference between adjacent elements
    avg_diff = sum(diffs) / len(diffs)
    
    # Create a new list representing the derivative of the vector
    derivative = [avg_diff] * len(vector)
    
    # Replace the first and last elements of the derivative with the adjacent differences
    derivative[0] = diffs[0]
    derivative[-1] = diffs[-1]
    
    return derivative

def replace_zeros(array, small_value=1e-12):
    """
    Replaces zeros in a NumPy array with a small value that can be accepted by the log10 function.
    
    Arguments:
    array -- a NumPy array
    small_value -- a small value to replace zeros with (default: 1e-10)
    
    Returns:
    replaced_array -- a NumPy array with zeros replaced by the small value
    """
    
    # Find the indices of the zeros in the array
    zero_indices = np.where(array == 0)
    
    # Create a copy of the array
    replaced_array = array.copy()
    
    # Replace the zeros with the small value
    replaced_array[zero_indices] = small_value
    
    return replaced_array

def remove_nans_infs(vector, small_value=1e-12):
    """
    Removes NaNs and Infs from a NumPy array and substitutes them with a small value and 0, respectively.
    
    Arguments:
    vector -- a NumPy array
    small_value -- a small value to replace NaNs with (default: 1e-12)
    
    Returns:
    cleaned_vector -- a NumPy array with NaNs and Infs replaced by the small value and 0, respectively
    """
    
    # Find the indices of the NaNs and Infs in the array
    nan_indices = np.where(np.isnan(vector))
    inf_indices = np.where(np.isinf(vector))
    
    # Create a copy of the array
    cleaned_vector = vector.copy()
    
    # Replace the NaNs with the small value
    cleaned_vector[nan_indices] = small_value
    
    # Replace the Infs with 0
    cleaned_vector[inf_indices] = 0
    
    return cleaned_vector

def max_slope_index(vector):

    """
    Finds the index with the maximum slope of a NumPy array.
    
    Arguments:
    vector -- a NumPy array
    
    Returns:
    max_slope_index -- the index with the maximum slope
    """
    
    # Compute the differences between adjacent elements of the array
    differences = np.diff(vector)
    
    # Compute the slopes of the array
    slopes = differences / vector[:-1]
    
    # Find the index with the maximum slope
    max_slope_index = np.argmax(slopes)
    
    return max_slope_index

def stretched_exponential(x, alpha, gamma, Vth_perm, Vth_pristine, Vth_max):
    return Vth_pristine+(Vth_max-Vth_perm)*np.exp(-x**gamma / alpha) + Vth_perm

def poly1(x,a,b):
    return a*x+b

#------------------------
# Main analysis functions
#------------------------

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
        times.append((j.time-data[0].time).total_seconds()) #Relative time from beginning of measure
    
    first_time = data[0].time
    #Calculate dose array
    dose = np.linspace(0,Total_dose, len(Vth))
    dose = np.asarray(dose, dtype="float64")

    #Return subthreshold slope
    ss = extraction_subthreshold_slope(data)

    #Linear fit to find sensitivity, when first derivative is zero
    islinear = np.where(dose>np.median(dose))[0]
    islinear = np.asarray(islinear, dtype=int)
    try:
        pl, el = curve_fit(poly1, np.asarray(dose)[islinear], np.asarray(Vth)[islinear])
        par = pl
        err = np.sqrt(np.diag(el))
    except:
        par = [1,1]
        err = [1,1]

    #Create the output dataframe
    output = {"Time": times, "Dose": dose, "Vth": Vth, "Mobility":Mu, "SS":ss }
    out = pd.DataFrame(output)
    return out, par, err, first_time

def extraction_subthreshold_slope(data: ct.Transfer):
    ss = []

    #First calculate the fitting range to find subthreshold slope
    #We can use the maximum slope as reference point and define a tolerance around it
    for i,j in enumerate(data):
        vg = j.VG
        j.ID = replace_zeros(j.ID)

        id = []
        for k,l in enumerate(j.ID):
            id.append(np.log10(l))
        id_prime = derivative(id)
        id_prime = remove_nans_infs(np.array(id_prime))
        max_id = max_slope_index(id)
        vg_max = vg[max_id]
        try:
            vg_low = max_id - int(max_id * 30/100)
            vg_high = max_id + int(max_id*30/100)
        except:
            vg_low = 200-10
            vg_high = 200-10

        #ss.append(j.calculate_subthreshold(vg_low, vg_high))
        ss.append(1)
    
    return ss

def recovery_analysis(data, initial_parameters, Vth_pristine, Vth_max):
    """
    Data should be a dataframe of the type returned by extract transfer data.

    This function fits the dataframe given as input with a stretched exponential to extract the parameters
    """

    #Initialize variables for fit
    X = data.Time
    Y = data.Vth
    
    
    #Define lambda function for fitting
    fit_func = lambda x, alpha, gamma, Vth_perm : stretched_exponential(x, alpha, gamma, Vth_perm, Vth_pristine, Vth_max)

    popt, pcov = curve_fit(fit_func, X, Y, p0=initial_parameters)

    err = np.sqrt(np.diag(pcov))

    fitted = fit_func(X, *popt)

    data_out = {"Time":X, "Vth": Y, "Fit": fitted}
    data_out_df = pd.DataFrame(data_out)

    return popt,err, data_out_df


