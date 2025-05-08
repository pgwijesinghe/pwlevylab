#%%
import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import butter, filtfilt

# Collect data files
folder_path = r"C:\Users\PubuduW\Desktop\20250417_InsTD_P_FullRange"
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

# Initialize lists to store relevant arrays
# time delay, photocurrent
delay_arr, pc_arr, = [], []

# Iterate through all TDMS files
for file_index, tdms_file_name in tqdm(enumerate(tdms_files), total=len(tdms_files), desc="Processing files", unit="file"):
    file_path = os.path.join(folder_path, tdms_file_name)
    
    # Read data from the TDMS file
    with nptdms.TdmsFile(file_path) as tdms_file:
        group = tdms_file["Data.000000"]
        delay = group["Delay"].data
        pc = group["Ch2_y"].data
        # pc = (pc - np.mean(pc)) / np.std(pc)  # z-score normalization

        # Convert delay to seconds
        delay_s = delay * 1e-12
        dt = np.mean(np.diff(delay_s))
        fs = 1 / dt
        nyq = 0.5 * fs

        # Define bandpass edges
        lowcut = 300e12  # in Hz
        highcut = 500e12  # in Hz
        low = lowcut / nyq
        high = highcut / nyq

        # Butterworth filter
        order = 1
        b, a = butter(order, [low, high], btype='band')
        pc = filtfilt(b, a, pc)

        if len(delay) == 70000 and len(pc) == 70000:
            delay_arr.append(delay)
            pc_arr.append(pc)

# Convert lists to numpy arrays for easy handling in plotting
delay_arr = np.array([x for x in delay_arr])
pc_arr = np.array([y for y in pc_arr])

# 2D plot: insertion vs TD
plt.figure(figsize=(10, 6))
plt.imshow(np.abs((pc_arr)), aspect='auto', cmap='plasma', origin='lower', vmin=0, vmax=2e-8)
plt.colorbar(label="Photovoltage Autocorrelation")
plt.xlabel('Delay Index')
plt.ylabel('File Index / Insertion')
plt.title('Insertion Length vs Time Delay')
plt.show()
