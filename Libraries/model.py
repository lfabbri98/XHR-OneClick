import numpy as np
from scipy.integrate import solve_ivp

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