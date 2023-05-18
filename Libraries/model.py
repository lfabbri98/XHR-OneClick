import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd

#Differential equation
def dydx(x,y, sens, IT, R, dvth0, gamma, alpha):
    """
    IT --> IRRADIATION TIME
    R --> DOSERATE
    """

    tau = alpha/gamma * (alpha * np.log(abs(dvth0/y)))**((1-gamma)/gamma)
    if x<IT:
        return sens*R-y/tau
    else:
        return -y/tau
    
def solve_xray(x, sens, IT,OT,TD,N, dvth0, gamma, alpha):
    """
    IT --> IRRADIATION TIME
    OT --> Total observation time of the measure (h)
    TD --> Totald dose

    Returns a vector containing the solution of the differential equation
    """
    R = TD/IT
    sol_func = lambda x,y: dydx(x,y, sens, IT, R, dvth0, gamma, alpha)
    sol = solve_ivp(sol_func, t_span = (0,OT*60*60), y0=[0], t_eval = np.linspace(0,OT*60*60,N))
    return sol.y[0,:]

def combine_model_data(irrad_data, recovery_data, recovery_first_time):
    """
    Input is composed of two dataframes for recovery and irradiation. It is important
    to have also the time execution of each measure to correctly shift the recovery with respect
    to irradiation.

    The dataframes should be in the format of the one returned from function extract_transfer_data
    """
    output_time = []
    output_vth = []
    output_dose = []

    for i in range(len(irrad_data)):
        output_time.append(irrad_data.Time[i])
        output_vth.append(irrad_data.Vth[i])
        output_dose.append(irrad_data.Dose[i])
    for i in range(len(recovery_data)):
        output_time.append(recovery_data.Time[i]+recovery_first_time.total_seconds())
        output_vth.append(recovery_data.Vth[i])
        output_dose.append(recovery_data.Dose[i])

    
    output_dict = {"Time": output_time, "Dose": output_dose, "Vth":output_vth}
    output_df = pd.DataFrame(output_dict)

    return output_df




def start_model_analysis(irrad_data, recovery_data, model_parameters, recovery_first_time):
    df = combine_model_data(irrad_data, recovery_data, recovery_first_time)
    return df

