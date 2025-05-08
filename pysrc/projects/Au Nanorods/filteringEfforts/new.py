'''
This is with the new TDMS format: Insertion and power are channels in the TDMS file.
'''

import os
import re
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import butter, filtfilt

# Folder with .tdms and .tdms_index files
folder_path = r"C:\Users\PubuduW\Desktop\20250430_HighRes_2"
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

delay_arr = None
pc_arr = []
insertion_arr = []
_GDD_per_mm = 20  # fs²/mm

# Process files
for tdms_file_name in tqdm(tdms_files, desc="Processing files"):
    tdms_path = os.path.join(folder_path, tdms_file_name)
    try:
        with nptdms.TdmsFile(tdms_path) as tdms_file:
            group = tdms_file["Data.000000"]
            delay = group["Delay"].data
            pc = group["Ch2_y"].data
            insertion = group["Insertion"].data[0]
            pc = (pc - np.mean(pc)) / np.std(pc)
            # pc = pc / np.max(np.abs(pc))

            # if len(delay) != 70000 or len(pc) != 70000:
            #     continue

            delay_s = delay * 1e-12
            # dt = np.mean(np.diff(delay_s))
            # fs = 1 / dt
            # nyq = 0.5 * fs

            # lowcut = 300e12
            # highcut = 500e12
            # b, a = butter(1, [lowcut / nyq, highcut / nyq], btype='band')
            # pc = filtfilt(b, a, pc)

            pc_arr.append(pc)
            insertion_arr.append(insertion)
            if delay_arr is None:
                delay_arr = delay_s

    except Exception as e:
        print(f"Error reading {tdms_file_name}: {e}")

# Check if any valid data
if delay_arr is None or len(pc_arr) == 0:
    print("No valid data loaded. Check file contents or insertion metadata.")
    exit()

# Convert insertion (mm) → GDD (fs²)
zero_insertion_point = 6.0  # Set this to the insertion value that should be 0 fs² GDD
gdd_arr = [(ins - zero_insertion_point) * _GDD_per_mm for ins in insertion_arr]
gdd_arr = np.array(gdd_arr)

# Sort arrays by GDD
sorted_indices = np.argsort(gdd_arr)
gdd_arr = gdd_arr[sorted_indices]
pc_arr = np.array(pc_arr)[sorted_indices]

# # Plot
# plt.figure(figsize=(10, 6))
# extent = [delay_arr[0]*1e12, delay_arr[-1]*1e12, gdd_arr[0], gdd_arr[-1]]  # Delay in ps, GDD in fs²
# plt.imshow(np.abs(pc_arr), aspect='auto', cmap='plasma', origin='lower', extent=extent, vmin=0, vmax=1)
# plt.colorbar(label="Normalized Photocurrent [A]")
# plt.xlabel('Delay (ps)')
# plt.ylabel('GDD (fs²)')
# # plt.title('GDD vs Time Delay')
# plt.tight_layout()
# plt.show()

# Plot (tick fix)
plt.figure(figsize=(10, 6))
extent = [delay_arr[0]*1e12, delay_arr[-1]*1e12, gdd_arr[0], gdd_arr[-1]]  # Delay in ps, GDD in fs²
plt.imshow(np.abs(pc_arr), aspect='auto', cmap='plasma', origin='lower', extent=extent)
plt.colorbar(label="Normalized Photocurrent [A]")
plt.xlabel('Delay (ps)')
plt.ylabel('GDD (fs²)')

# Set Y-axis ticks every 100 fs²
plt.yticks(np.arange(np.floor(gdd_arr[0]/100)*100, np.ceil(gdd_arr[-1]/100)*100 + 1, 100))

plt.tight_layout()
plt.show()