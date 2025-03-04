#%%
import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# instrument = 'THz 1'
# device = 'SA40653C.20250123'
# measurement = '02 - Delay vs Insertion'

instrument = 'THz 1'
device = 'SA40653C.20250123'
measurement = '11 - 0203\TD vs Insertion'

# Collect data files
folder_path = f"G:\\.shortcut-targets-by-id\\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\\ansom\\Data\\{instrument}\\{device}\\{measurement}"
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

# Initialize lists to store relevant arrays
# time delay, photovoltage, frequency, power spectrum
delay_arr, pv_arr, freq_arr, ps_arr = [], [], [], []

# Iterate through all TDMS files
for file_index, tdms_file_name in tqdm(enumerate(tdms_files), total=len(tdms_files), desc="Processing files", unit="file"):
    file_path = os.path.join(folder_path, tdms_file_name)
    
    # Read data from the TDMS file
    with nptdms.TdmsFile(file_path) as tdms_file:
        group = tdms_file["Data.000000"]
        delay = group["Delay"].data
        pv = group["Ch6_y"].data
        freq = group["Ch6_PS_x"].data
        ps = group["Ch6_PS_y"].data

        # TD
        delay_arr.append(delay[0:100000]) #previously 19000
        pv_arr.append(pv[0:100000])

        # PS: Slice the arrays to keep only values where x <= 1200
        slice_index = np.where(freq <= 1200)[0][-1]  # Get the index of the last value where x <= 1200
        slice_index = 1000 #previously 120
        freq_arr.append(freq[20:slice_index + 1])
        ps_arr.append(ps[20:slice_index + 1])

# Convert lists to numpy arrays for easy handling in plotting
delay_arr = np.array([x for x in delay_arr])
pv_arr = np.array([y for y in pv_arr])
freq_arr = np.array([x for x in freq_arr])
ps_arr = np.array([y for y in ps_arr])

# 2D plot: insertion vs TD
plt.figure(figsize=(10, 6))
plt.imshow(pv_arr, aspect='auto', cmap='plasma', extent=[delay_arr.min(), delay_arr.max(), 0, len(tdms_files)])
plt.colorbar(label="Photovoltage Autocorrelation")
plt.xlabel('Time Delay (ps)')
plt.ylabel('File Index/Insertion')
plt.title('Insertion Length vs Time Delay')

# # 2D plot: insertion vs power spectrum (commenting out to include the WL below)
# plt.figure(figsize=(10, 6))
# plt.imshow(np.log(ps_arr), aspect='auto', cmap='plasma', extent=[freq_arr.min(), freq_arr.max(), 0, len(tdms_files)])
# plt.colorbar(label="Device Power Spectral Intensity")
# plt.xlabel('Frequency (THz)')
# plt.ylabel('File Index')
# plt.title('File Index vs Power Spectrum')

# Convert frequencies to wavelengths in nm
wavelength_arr = (3.0e8 / (freq_arr * 1e12)) * 1e9  # Convert from THz to Hz, then from meters to nm

# 2D plot: insertion vs power spectrum with second x-axis for wavelength
fig, ax1 = plt.subplots(figsize=(10, 6))

cax = ax1.imshow(np.log(ps_arr), aspect='auto', cmap='plasma', extent=[freq_arr.min(), freq_arr.max(), 0, len(tdms_files)])
ax1.set_xlabel('Frequency (THz)')
ax1.set_ylabel('File Index')
ax1.set_title('File Index vs Power Spectrum')
fig.colorbar(cax, ax=ax1, label="Device Power Spectral Intensity")

# Create a second x-axis for wavelength
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())  # Same limits as the first x-axis
ax2.set_xlabel('Wavelength (nm)')

# Set the ticks for the second x-axis
ax2.set_xticks(np.linspace(freq_arr.min(), freq_arr.max(), num=6))  # You can adjust the number of ticks
ax2.set_xticklabels(np.round((3.0e8 / (np.linspace(freq_arr.min(), freq_arr.max(), num=6) * 1e12)) * 1e9, 2))  # Convert to wavelength

plt.show()

# %%
