import Libraries.classTransfer as ct
import pandas as pd
import Libraries.data_read as dr
import matplotlib.pyplot as plt
import Libraries.transfer_analysis as ta
import Libraries.model as model
import os
import datetime as dt


def main(Irrad_path, Rec_path, Cox, W, L, Total_dose, outputpath,N,Ntrans, configuration_file):
    irrad = dr.read_folder(Irrad_path)
    irrad_data, irrad_par, irrad_err, irrad_first_time = ta.extract_transfer_data(irrad, Cox, W, L, Total_dose,N)
    Vth_pristine = irrad_data.Vth[0]
    Vth_max = irrad_data.Vth.values[-1]-irrad_data.Vth[0]

    #Figure 1: plot of transfers in linear scale and log scale
    fig, (ax11, ax12)  = plt.subplots(1,2)
    fig.canvas.manager.set_window_title('Irradiation')
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

    #Add plot of recovery transfers and plot only N transfers

    #Figure 2: Plot of threshold variation in function of dose
    fig2, ax2 = plt.subplots()
    fig2.canvas.manager.set_window_title('Irradiation')
    ax2.plot(irrad_data.Dose, irrad_data.Vth, label="Data")
    ax2.plot(irrad_data.Dose, ct.poly1(irrad_data.Dose, *irrad_par ), label="Linear fit")
    ax2.set_xlabel("Dose (Gy)")
    ax2.set_ylabel("$V_{th}$ (V)")
    ax2.set_title("Threshold in function of dose")
    ax2.legend(loc='best')
    fig2.tight_layout()

    #Figure 3: Plot of mobility and subthreshold variation in function of dose
    fig3, (ax31, ax32, ax33) = plt.subplots(1,3)
    fig3.canvas.manager.set_window_title('Irradiation')
    ax31.plot(irrad_data.Dose, irrad_data.Mobility)
    ax32.plot(irrad_data.Dose, irrad_data.SS, ls='none', marker='o')
    ax33.plot(irrad_data.Dose, irrad_data.Von, ls='none', marker='o')
    ax33.set_xlabel("Dose (Gy)")
    ax33.set_ylabel("$V_{on}$ (V)")
    ax31.set_xlabel("Dose (Gy)")
    ax31.set_ylabel("$\mu (cm^2 /Vs)$")
    ax31.set_title("Mobility")
    ax32.set_xlabel("Dose (Gy)")
    ax32.set_ylabel("Subthreshold slope (V/dec)")
    ax32.set_title("Subthreshold slope")
    ax32.set_ylim(0)
    ax33.set_title("Von")
    fig3.tight_layout()

    #Recovery
    rec = dr.read_folder(Rec_path)
    use_custom_params, p0_rec = ct.read_recovery_fit(configuration_file)
    rec_analyzed, recovery_par, recovery_err, recovery_first_time = ta.extract_transfer_data(rec, Cox, W, L, Total_dose,N)
    
    #Add last point of irradiation
    last = irrad_data.values[-1]
    first_time = last[0]
    ft = (recovery_first_time-irrad[0].time).total_seconds()
    last[0] = last[0]-(recovery_first_time-irrad[0].time).total_seconds()
    rec_analyzed.loc[-1] = last
    rec_analyzed.index = rec_analyzed.index+1
    rec_analyzed.sort_index(inplace=True)
    
    
    for i in range(len(rec_analyzed)):
        rec_analyzed.Time[i]= rec_analyzed.Time[i] + abs(first_time)


    rec_analyzed_fit = rec_analyzed
    rec_analyzed_fit.Time = rec_analyzed_fit.Time-rec_analyzed_fit.Time[0]
    params, errors, rec_fit = ta.recovery_analysis(rec_analyzed_fit, p0_rec, Vth_pristine, Vth_max)
    

    #Figure 4: Scatter plot of recovery with stretched exponential fit
    fig4, ax4 = plt.subplots()
    fig4.canvas.manager.set_window_title('Recovery')
    ax4.plot((rec_analyzed.Time+ft)/3600, rec_fit.Vth, marker = 'o', label="Experimental data")
    ax4.plot((rec_analyzed.Time+ft)/3600, rec_fit.Fit, label="Stretched exponential fit")
    ax4.set_xlabel("Time (h)")
    ax4.set_ylabel("$V_{th}$ (V)")
    ax4.set_title("Recovery")
    plt.legend(loc='best')

    #Figure 5: Plot of mobility and subthreshold variation in function of dose during recovery
    fig5, (ax51, ax52, ax53) = plt.subplots(1,3)
    fig5.canvas.manager.set_window_title('Recovery')
    ax51.plot((rec_analyzed.Time+ft)/3600, rec_analyzed.Mobility)
    ax52.plot((rec_analyzed.Time+ft)/3600, rec_analyzed.SS, ls='none', marker='o')
    ax53.plot((rec_analyzed.Time+ft)/3600, rec_analyzed.Von, ls='none', marker='o')
    ax53.set_xlabel("Time (h)")
    ax53.set_ylabel("$V_{on}$ (V)")
    ax51.set_xlabel("Time (h)")
    ax51.set_ylabel("$\mu (cm^2 /Vs)$")
    ax51.set_title("Mobility")
    ax52.set_xlabel("Time (h)")
    ax52.set_ylabel("Subthreshold slope (V/dec)")
    ax52.set_title("Subthreshold slope")
    ax53.set_title("Von")
    ax52.set_ylim(0)
    fig5.tight_layout()

    
    #Create file with output parameters
    names_params = ["Type","Sensitivity (V/Gy)", "alpha (1/h)", "gamma", "Vth_perm (V)"]
    line_1 = ["Parameter",irrad_par[0], params[0], params[1], params[2]]
    line_2 = ["Error",irrad_err[0],errors[0], errors[1], errors[2]]
    df  = [names_params, line_1, line_2]

    output_params = pd.DataFrame(df)

    #File ouput
    #Creation of output directory, check if existent
    directory_name = outputpath

# Check if the directory already exists
    if not os.path.exists(directory_name):
    # If it does not exist, create it
        os.makedirs(directory_name)
    print("Directory", directory_name, "created.")

    irrad_data.to_csv(directory_name+"Irradiation_transfer_analysis.txt", sep="\t")
    rec_fit.to_csv(directory_name+"Recovery_output.txt", sep="\t")
    output_params.to_csv(directory_name+"Parameters_output.txt", sep="\t")
    rec_analyzed.to_csv(directory_name+"Recovery_transfer_analysis", sep="\t")

    plt.show()