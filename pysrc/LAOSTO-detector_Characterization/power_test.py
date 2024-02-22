'''
Varying the intensity with time with the HWP, measuring APD response and the device response and plotting them one vs. another
'''
import os
import nptdms
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.signal import find_peaks

# Set the path to the folder containing the TDMS files
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Power Test\E2\SA40287.20231121.000006.tdms"
# file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Power Test\HeNe\SA40287.20231121.000005.tdms"

#05,06
# 260uw

# Read Data
with nptdms.TdmsFile(file_path) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group1 = tdms_file["Data.000000"]
    APD_y = group1["AI8"].data # apd signal
    Device_y = group1["X2"].data # photovoltage of the device
    time = group1["Time"].data

#smoothen the apd signal
from scipy.signal import savgol_filter
Device_y = savgol_filter(Device_y, 5, 2)
APD_y = savgol_filter(APD_y, 5, 2)

plt.figure()
plt.plot(time, APD_y, color='blue',label="APD")

plt.figure()
plt.plot(time, Device_y, color='red',label="LAO/STO")

plt.figure()
plt.plot(APD_y[4:], Device_y[4:], color='blue',label="APD")

plt.show()