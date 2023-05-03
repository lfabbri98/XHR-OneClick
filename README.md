# XHR - OneClick

## Introduction
This program performs the analysis of x-ray hardness and recovery data. The input of the program is just a series of parameters decided from the user and the paths of irradiation and recovery folders. All the required parameters are explained below. 

The program gives as ouput some plots and edited data which can be useful to further edit them or make combined plots.

## Usage
### 1. Fill the configuration file
The default configuration file is contained in the folder and called *config.txt*.

Many configuration files can be created to perform the analysis without modifing every time the file.
We suggest to copy it to avoid to accidentaly modify its structure. In case, the file becomes unusable.

Each configuration file must be divided in some sections:
- **[settings]** contains all the parameters for the transfer analysis part, such as the directory paths, oxide capacitance, width, length of the channel and the total dose received
- **[recovery]** can be used to decide if the initial parameters of recovery fit are chosen automatically (do not rely too much on them) or provided by the user
- **[output]** section can be used to decide where to save the ouput files. The program checks if the directory already exists and if not, creates it. If the folder already exists, it will be overwritten.

### 2. Start the program
To start the analysis, open the python file **start_analysis.py** and change the path of configuration file in the first section. *Do not modify all the lines below!*

 
