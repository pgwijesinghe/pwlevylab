import matplotlib.style
from nptdms import TdmsFile
import matplotlib.pyplot as plt
import matplotlib
import re
import numpy as np
import pandas as pd
import os
matplotlib.style.use('ggplot')
import glob

sweep_folder_path = r"C:\Users\PubuduW\Desktop\06 - IV vs Power"

wiring_dict = {'I+': 1, 'I-': 3, 'dV1': 2}

import re

def extract_sweepparams(index):
    with open(index, 'r', encoding='Latin-1') as file:
        data = file.read()

    # Pattern to match the entire block after "Sweep:" and before the next unindented section
    pattern = re.compile(r'Sweep:\s*((?:- Loop\d+: \[.*?\]\s*)+)', re.DOTALL)
    match = pattern.search(data)

    if match:
        sweep_block = match.group(1).strip()
        sweep_lines = sweep_block.split('\n')
    
        extracted_info = {}
        line_pattern = re.compile(r'- Loop(\d+): \[(.*?), ([\d.-]+)\]')  # Adjusted pattern to capture values
        
        for line in sweep_lines:
            match_line = line_pattern.search(line.strip())
            if match_line:
                loop_number = 'Loop' + match_line.group(1)
                label = match_line.group(2).strip()
                value = float(match_line.group(3))
                extracted_info[loop_number] = [label, value]
        
        return extracted_info
    else:
        print("Sweep information not found.")
        return None

def plot_IV_sweep(type, datafile, savetoCSV=False):
    index_file = datafile + "_index"
    # sweep_value = extract_sweepparams(index_file)['Loop1'][1]
    with TdmsFile.open(tdms_file_path) as tdms_file:
        Iplus_lead = wiring_dict['I+']
        Iminus_lead = wiring_dict['I-']
        Iplus = tdms_file[tdms_file.groups()[0].name][f'AI{Iplus_lead}'][:]
        Iminus = tdms_file[tdms_file.groups()[0].name][f'AI{Iminus_lead}'][:]
        Vsource = tdms_file[tdms_file.groups()[0].name][f'AO{Iplus_lead}'][:]
        if 'dV1' in wiring_dict:
            dV_lead = wiring_dict['dV1']
            dV = tdms_file[tdms_file.groups()[0].name][f'AI{dV_lead}'][:]
        elif 'V1+' in wiring_dict and 'V1-' in wiring_dict:
            Vplus_lead = wiring_dict['V1+']
            Vminus_lead = wiring_dict['V1-']
            dV = tdms_file[tdms_file.groups()[0].name][f'AI{Vplus_lead}'][:] - tdms_file[tdms_file.groups()[0].name][f'AI{Vminus_lead}'][:]
        
        if type == '2T':
            plt.plot(Vsource, Iminus)
            plt.xlabel('Source Voltage (V)')
            plt.ylabel('Current (A)')
        elif type == '4T':
            plt.plot(dV, Iminus)
            plt.xlabel('Source Voltage (V)')
            plt.ylabel('Current (A)')
        
        if savetoCSV:
            data = pd.DataFrame({'Vsource':Vsource, 'dV':dV, 'Iminus':Iminus})
            data.to_csv(f'{os.path.splitext(datafile)[0]}_toIgor.csv', index=False)

plt.figure()
for tdms_file_path in glob.glob(sweep_folder_path + r"\*.tdms"):
    print(f'{tdms_file_path} processed')
    plot_IV_sweep('4T', datafile=tdms_file_path, savetoCSV=True)
plt.legend()
plt.show()

