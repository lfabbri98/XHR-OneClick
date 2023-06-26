"""
Use this file to configure and start the execution of XRH analysis.
"""
#------------------------
# Configuration file 
#------------------------

configuration_file = "./config.txt"

### DO NOT MODIFY UNDER THIS LINE
#------------------------
# Check and eventually install missing packages
#------------------------
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("numpy")
install("matplotlib")
install("scipy")
install("configparser")
install("pandas")

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

Libraries.main.main(Irrad_path, Rec_path, Cox, W, L, Total_dose, outputpath,N,Ntrans, configuration_file)