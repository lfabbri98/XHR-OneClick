"""
Use this file to configure and start the execution of XRH analysis.
"""
#------------------------
# Configuration file 
#------------------------

configuration_file = "./config.txt"

### DO NOT MODIFY UNDER THIS LINE

#------------------------
# Import libraries
#------------------------

import Libraries.main
import Libraries.classTransfer

#------------------------
# Read parameters
#------------------------

Irrad_path, Rec_path, Cox, W, L, Total_dose, outputpath,N,Ntrans = Libraries.classTransfer.import_parameters(config_path=configuration_file)

#------------------------
# Start execution
#------------------------

Libraries.main.main(Irrad_path, Rec_path, Cox, W, L, Total_dose, outputpath,N, configuration_file)