import os
import re
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from scipy.signal import butter, filtfilt

def extract_insertion_power(file_path):
    if not os.path.exists(file_path):
        return None  # skip if metadata file doesn't exist
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    match = re.search(r'Insertion\s*=\s*([0-9.+-eE]+)\s*:\s*Power\s*=\s*([0-9.+-eE]+)', content)
    return float(match.group(1)) if match else None

# Collect data files
folder_path = r"C:\Users\PubuduW\Desktop\20250417_InsTD_P_FullRange"
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

delay_arr, pc_arr, insertion_arr = [], [], []

# Iterate through TDMS files
for tdms_file_name in tqdm(tdms_files, desc="Processing files"):
    tdms_path = os.path.join(folder_path, tdms_file_name)
    tdms_index_path = tdms_path.replace('.tdms', '.tdms_index')
    insertion = extract_insertion_power(tdms_index_path)
    if insertion is None:
        continue

    with nptdms.TdmsFile(tdms_path) as tdms_file:
        group = tdms_file["Data.000000"]
        delay = group["Delay"].data
        pc = group["Ch2_y"].data
        pc = (pc - np.mean(pc))/np.std(pc)  # z-score normalization

        delay_s = delay * 1e-12
        # dt = np.mean(np.diff(delay_s))
        # fs = 1 / dt
        # nyq = 0.5 * fs

        # lowcut = 300e12
        # highcut = 500e12
        # b, a = butter(1, [lowcut / nyq, highcut / nyq], btype='band')
        # pc = filtfilt(b, a, pc)

        if len(delay) == 70000 and len(pc) == 70000:
            pc_arr.append(pc)
            insertion_arr.append(insertion)
            delay_arr = delay_s

# Sort everything by insertion
sorted_indices = np.argsort(insertion_arr)
insertion_arr = np.array(insertion_arr)[sorted_indices]
pc_arr = np.array(pc_arr)[sorted_indices]

# Plot
plt.figure(figsize=(10, 6))
extent = [delay_arr[0]*1e12, delay_arr[-1]*1e12, insertion_arr[0], insertion_arr[-1]]  # x in ps
plt.imshow(np.abs(pc_arr), aspect='auto', cmap='plasma', origin='lower', extent=extent, vmin=0, vmax=2e-8)
plt.colorbar(label="Photovoltage Autocorrelation")
plt.xlabel('Delay (ps)')
plt.ylabel('Insertion (mm)')
plt.title('Insertion Length vs Time Delay')
plt.show()
