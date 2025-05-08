import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import savgol_filter
import re

file_path = r"C:\Users\PubuduW\Desktop\20250417_InsTD_P_FullRange\SA40663G.20250403.000035.tdms"

with nptdms.TdmsFile(file_path) as tdms_file:
    group = tdms_file["Data.000000"]
    delay = group["Delay"].data
    pc = group["Ch2_y"].data
    # pc = savgol_filter(pc, window_length=51, polyorder=3)
    
from scipy.signal import butter, filtfilt

# # Convert delay to seconds
# delay_s = delay * 1e-12
# dt = np.mean(np.diff(delay_s))
# fs = 1 / dt
# nyq = 0.5 * fs

# # Define bandpass edges
# lowcut = 300e12 # in Hz
# highcut = 500e12  # in Hz
# low = lowcut / nyq
# high = highcut / nyq

# # Butterworth filter
# order = 3
# b, a = butter(order, [low, high], btype='band')
# pc_filtered = filtfilt(b, a, pc)
# pc = savgol_filter(pc_filtered, window_length=1001, polyorder=3)

# Plot
plt.plot(delay, pc, color='green')
plt.xlabel("Delay (ps)")
plt.ylabel("Photocurrent (A)")
# plt.title("Photocurrent (380–480 THz Bandpass)")
plt.grid(True)
plt.show()

