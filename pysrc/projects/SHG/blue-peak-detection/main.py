'''
Characterizing the SHG signal reflected off from the BBO/interferometer setup.
Purpose is to compare IR vs. SHG Peak Trends as a function of z to check whether there's a optimal z point for SHG
This is an experiment where I got interferometric data from a BBO and tried to analyze the blue peak trend as a function of z and compare it to the IR peak trend
Optical flow: E2 → Prism pair → Chirp Mirrors → Interferometer → BBO → (Reflection) → Dichroic Mirror → Blue filter → APD
'''

import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# Set the path to the folder containing the TDMS files
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Pubudu's Data\10 - blue peak analysis"

# Create empty lists to store the arrays
array1 = []
array2 = []

# Define the z array
z = np.linspace(35, 80, 16)
print(z)

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".tdms"):
        # Load the TDMS file
        with nptdms.TdmsFile(os.path.join(folder_path, filename)) as tdms_file:
            # Get the group and channel names for the two arrays you want to extract
            group1 = tdms_file["Data.000000"]
            channel1 = group1["Ch8_PS_y"]
            
            # Append the data from each channel to the corresponding list
            array1.append(channel1[:])

# Define the x ranges
x_range1 = (200,235)
x_range2 = (415, 460)

# Create empty lists to store the max peaks
max_peaks1 = []
max_peaks2 = []

# Loop through all arrays in array1
for i in range(len(array1)):
    # Convert the array to log scale
    log_array = np.log(array1[i])
    
    # Find the indices of the highest peaks in the two x ranges
    peaks1, _ = find_peaks(log_array[x_range1[0]:x_range1[1]], height=np.max(log_array)-8)
    peaks2, _ = find_peaks(log_array[x_range2[0]:x_range2[1]], height=np.max(log_array)-8)
    
    # Add the x range offsets to the peak indices
    peaks1 += x_range1[0]
    peaks2 += x_range2[0]
    
    # Append the max peaks to the corresponding list
    max_peaks1.append(np.max(log_array[peaks1]))
    max_peaks2.append(np.max(log_array[peaks2]))

# Plot the max peaks of each range as a function of array1 index in the same plot
plt.plot(z,max_peaks1, color='orange', label="IR")
plt.plot(z,max_peaks2, color='blue', label="Blue")
plt.xlabel("z (um)")
plt.ylabel("Max peak")
plt.legend()
plt.show()

