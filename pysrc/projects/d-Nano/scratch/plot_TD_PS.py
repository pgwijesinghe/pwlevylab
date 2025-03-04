
"""
Analyzing the Interferometric Autocorrelation Fourier Transform Spectroscopy Data vs. d-Micro insertion
"""

import nptdms
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.signal import find_peaks

# Set the path to the folder containing the TDMS files
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250123\11 - 0203\TD vs Insertion\SA40653C.20250123.000011.tdms"
file_path2 = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250123\11 - 0203\TD vs Insertion\SA40653C.20250123.000003.tdms"
insertion_length = np.linspace(10, 20, 51)

# Read Data
with nptdms.TdmsFile(file_path) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group = tdms_file["Data.000000"]
    delay = group["Delay"].data
    device_TD = group["Ch6_y"].data
    x = group["Ch6_PS_x"].data
    device_PS = group["Ch6_PS_y"].data

with nptdms.TdmsFile(file_path2) as tdms_file2:
    # Get the group and channel names for the two arrays you want to extract
    group = tdms_file2["Data.000000"]
    delay2 = group["Delay"].data - 0.004
    device_TD2 = group["Ch6_y"].data + 0.0003
    x2 = group["Ch6_PS_x"].data
    device_PS2 = group["Ch6_PS_y"].data
      

plt.figure()
plt.plot(delay, device_TD, delay2, device_TD2)
plt.show()

plt.figure()
plt.plot(x, np.log(device_PS))
plt.xlim(0,1200)
plt.show()





