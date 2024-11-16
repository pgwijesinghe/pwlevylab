import matplotlib.style
from nptdms import TdmsFile
import matplotlib.pyplot as plt
import matplotlib
import re
import numpy as np
import pandas as pd
import os
matplotlib.style.use('ggplot')

# tdms_file_path = r"D:\Data\CF900\SA40458.20240606\01 - IV\SA40458.20240606.000008.tdms"
tdms_file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40526J.20241030\01 - IV\SA40526J.20241030.000005.tdms"
index_file = tdms_file_path + "_index"

def extract_wiring(index):
    with open(index, 'r') as file:
        data = file.read()

    pattern = re.compile(r'Wiring:\s*(.*?)\s*Lockin:', re.DOTALL)
    match = pattern.search(data)

    if match:
        wiring_block = match.group(1).strip()
        wiring_lines = wiring_block.split('\n')
        line_pattern = re.compile(r'Lockin (\d+), (.+)$')       
        extracted_info = {}
        
        for line in wiring_lines:
            match_line = line_pattern.search(line.strip())
            if match_line:
                lockin_number = match_line.group(1)
                label = match_line.group(2)
                extracted_info[label] = lockin_number
        return extracted_info
    else:
        print("Wiring information not found.")

def plot_IV(type='2T', datafile=tdms_file_path, savetoCSV=False):
    index_file = tdms_file_path + "_index"
    wiring_dict = extract_wiring(index_file)
    print(wiring_dict)
    with TdmsFile.open(tdms_file_path) as tdms_file:
        Iplus_lead = 1
        Iminus_lead = 3
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
        plt.figure()
        if type == '2T':
            print("Plotting 2T IV...")
            plt.plot(Vsource, Iminus)
            plt.xlabel('Source Voltage (V)')
            plt.ylabel('Current (A)')
        elif type == '4T':
            print("Plotting 4T IV...")
            plt.plot(dV, Iminus)
            plt.xlabel('Source Voltage (V)')
            plt.ylabel('Current (A)')
        # plt.hlines(0,-5e-3,5e-3,colors='black')
        # plt.vlines(0,-1e-7,1e-7,colors='black')
        plt.show()

        if savetoCSV:
            data = pd.DataFrame({'Vsource':Vsource, 'dV':dV, 'Iminus':Iminus})
            data.to_csv(f'{os.path.splitext(datafile)[0]}_toIgor.csv', index=False)

plot_IV('4T', datafile=tdms_file_path, savetoCSV=False)
