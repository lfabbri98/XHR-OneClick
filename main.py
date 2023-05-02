import classTransfer as ct
import pandas as pd
import data_read as dr
import matplotlib.pyplot as plt
import transfer_analysis as ta
import os


def main(Irrad_path, Rec_path, Cox, W, L, Total_dose, outputbool, outputpath):
    irrad = dr.read_folder(Irrad_path)
    irrad_data = ta.extract_transfer_data(irrad, Cox, W, L, Total_dose)

    #Figure 1: plot of transfers in linear scale and log scale
    fig, (ax11, ax12)  = plt.subplots(1,2)
    for i in irrad:
        ax11.plot(i.VG, i.ID/1e-6)
        ax12.plot(i.VG, i.ID)
    ax11.set_xlabel("$V_G$ (V)")
    ax11.set_ylabel("$I_D (\mu A)$")
    ax11.set_title("Transfers in linear scale")
    ax12.set_xlabel("$V_G$ (V)")
    ax12.set_ylabel("$I_D$ (A)")
    ax12.set_yscale("log")
    ax12.set_title("Transfers in log scale")

    fig.tight_layout()

    #Figure 2: Plot of threshold variation in function of dose
    fig2, ax2 = plt.subplots()
    ax2.plot(irrad_data.Dose, irrad_data.Vth)
    ax2.set_xlabel("Dose (Gy)")
    ax2.set_ylabel("$V_{th}$ (V)")
    ax2.set_title("Threshold in function of dose")
    fig2.tight_layout()

    print("Threshold shift = ",irrad_data.Vth.values[-1]-irrad_data.Vth[0],"V")

    #Figure 3: Plot of mobility and subthreshold variation in function of dose
    fig3, (ax31, ax32) = plt.subplots(1,2)
    ax31.plot(irrad_data.Dose, irrad_data.Mobility)
    ax32.plot(irrad_data.Dose, irrad_data.SS)
    ax31.set_xlabel("Dose (Gy)")
    ax31.set_ylabel("$\mu (cm^2 /Vs)$")
    ax31.set_title("Mobility")
    ax32.set_xlabel("Dose (Gy)")
    ax32.set_ylabel("Subthreshold slope (V/dec)")
    ax32.set_title("Subthreshold slope")
    fig3.tight_layout()

    #File ouput
    #Creation of output directory, check if existent
    directory_name = outputpath

# Check if the directory already exists
    if not os.path.exists(directory_name):
    # If it does not exist, create it
        os.makedirs(directory_name)
    print("Directory", directory_name, "created.")


    irrad_data.to_csv(directory_name+"Transfer_results.txt", sep="\t")

    plt.show()