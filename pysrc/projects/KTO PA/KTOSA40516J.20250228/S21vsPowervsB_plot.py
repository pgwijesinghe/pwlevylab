import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm
from scipy.fftpack import fft, ifft, fftfreq
from collections import defaultdict

# Path to the folder containing all the TDMS files
folder_path = r"C:\Users\pubud\Desktop\10-B Power S21-20250304T111345Z-001\10-B Power S21"

# Function to process each TDMS file and extract necessary data
def process_tdms_file(file_path):
    tdms_file = TdmsFile.read(file_path)
    group = tdms_file["Data.000000"]
    
    # Extract frequency, ReS21, ImS21, and Magnet data
    frequency = group["frequency"].data
    re_s21 = group["ReS21"].data
    im_s21 = group["ImS21"].data
    magnet = round(group["Magnet"].data[0], 2)
    power = group["P"].data[0]
    
    # Compute magnitude and log-magnitude of S21
    magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
    log_mag_s21 = 20 * np.log10(magnitude_s21)
    
    return magnet, frequency, log_mag_s21, power

# Dictionary to store data: {magnetic_field: {power: (frequencies, S21 values)}}
data_by_magnetic_field = defaultdict(lambda: defaultdict(list))

# Iterate through all the TDMS files in the directory
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])

for file_name in tqdm(file_list, desc="Processing TDMS files"):
    file_path = os.path.join(folder_path, file_name)
    
    magnet, frequencies, log_magnitude_s21, power = process_tdms_file(file_path)
    
    # Store frequency and log(S21) values indexed by magnetic field and power
    data_by_magnetic_field[magnet][power].append((frequencies, log_magnitude_s21))

# Dictionary to store magnetic field vs power of minimum S21
magnetic_fields_and_powers = {}

# Process the data for each unique magnetic field
for magnet, power_dict in data_by_magnetic_field.items():
    all_powers = sorted(power_dict.keys())
    all_frequencies = None
    
    # Create an empty heatmap for S21 values
    heatmap = []
    
    for power in all_powers:
        freq_list, s21_list = zip(*power_dict[power])  # Unpack frequency & S21 data
        avg_s21 = np.mean(s21_list, axis=0)  # Average over multiple measurements if needed
        
        if all_frequencies is None:
            all_frequencies = freq_list[0]  # Assume all have same frequencies
        
        heatmap.append(avg_s21)  # Store S21 data row-wise
    
    heatmap = np.array(heatmap)  # Convert to 2D array
    all_powers = np.array(all_powers)  # Convert to array for indexing
    
    # Find global minimum S21 in the heatmap
    min_idx = np.unravel_index(np.argmin(heatmap), heatmap.shape)
    min_power = all_powers[min_idx[0]]
    min_freq = all_frequencies[min_idx[1]]
    min_value = heatmap[min_idx]

    # print(f"Magnetic Field: {magnet} T, Minimum S21: {min_value:.2f} dB, Power: {min_power} dBm, Frequency: {min_freq:.2f} Hz")

    magnetic_fields_and_powers[magnet] = min_power

# Plot the magnetic field vs power
magnetic_fields = list(magnetic_fields_and_powers.keys())
powers = list(magnetic_fields_and_powers.values())
print(magnetic_fields)
idx = [1, 4, 6, 8, 10, 13, 16, 19, 22, 25]
x = magnetic_fields
y = powers
plt.figure(figsize=(8, 6))
plt.plot(x,y, marker='o', linestyle='-', color='b')
plt.xlabel('Magnetic Field (T)')
plt.ylabel('Power corresponding to minimum S21 (dBm)')
plt.title('Magnetic Field vs Power for Minimum S21')
plt.grid(True)
plt.show()
