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
file_path1 = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Power Test\E2\SA40287.20231121.000006.tdms"
file_path2 = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Power Test\E2\SA40287.20231121.000007.tdms"
# file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Power Test\HeNe\SA40287.20231121.000005.tdms"

#05,06

# Read Data
with nptdms.TdmsFile(file_path1) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group11 = tdms_file["Data.000000"]
    APD_y1 = group11["AI8"].data # apd signal
    Device_y1 = group11["X2"].data # photovoltage of the device
    time1 = group11["Time"].data

with nptdms.TdmsFile(file_path2) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group12 = tdms_file["Data.000000"]
    APD_y2 = group12["AI8"].data # apd signal
    Device_y2 = group12["X2"].data # photovoltage of the device
    time2 = group12["Time"].data

#smoothen the apd signal
from scipy.signal import savgol_filter
Device_y1 = savgol_filter(Device_y1, 5, 2)
APD_y1 = savgol_filter(APD_y1, 5, 2)
Device_y2 = savgol_filter(Device_y2, 5, 2)
APD_y2 = savgol_filter(APD_y2, 5, 2)

plt.figure()
plt.plot(time1, APD_y1, color='blue',label="APD")
plt.plot(time2, APD_y2, color='blue',label="APD")

plt.figure()
plt.plot(time1, Device_y1, color='blue',label="APD")
plt.plot(time2, Device_y2, color='red',label="LAO/STO")

plt.figure()
plt.plot(APD_y1[4:], Device_y1[4:], color='blue',label="APD")
plt.plot(APD_y2[4:], Device_y2[4:], color='blue',label="APD")


plt.show()