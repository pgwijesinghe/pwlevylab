import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import savgol_filter

file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40663G.20250429\20250430_HighRes_2\SA40663G.20250429.000180.tdms"

with nptdms.TdmsFile(file_path) as tdms_file:
    group = tdms_file["Data.000000"]
    delay = group["Delay"].data
    pc = group["Ch2_y"].data

from scipy.signal import savgol_filter

# Adjust window_length and polyorder as needed
smoothed = savgol_filter(pc, window_length=501, polyorder=3)

plt.figure(figsize=(10, 4))
plt.plot(delay, pc, label='Original Signal')
plt.plot(delay, smoothed, label='Smoothed (Savitzky-Golay)', color='green', linewidth=2)
plt.legend()
plt.title("Smoothed Signal as Envelope")
plt.xlabel("Delay")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
