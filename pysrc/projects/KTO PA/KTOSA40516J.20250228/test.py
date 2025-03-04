import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm
from scipy.fftpack import fft, ifft, fftfreq

# Path to the folder containing all the TDMS files
folder_path = r"C:\Users\pubud\Desktop\10-B Power S21-20250304T100447Z-001\10-B Power S21"

# Function to process each TDMS file and extract necessary data
def process_tdms_file(file_path):
    tdms_file = TdmsFile.read(file_path)
    group = tdms_file["Data.000000"]
    
    # Extract frequency, ReS21, ImS21, and Magnet data
    frequency = group["frequency"].data
    re_s21 = group["ReS21"].data
    im_s21 = group["ImS21"].data
    magnet = group["Magnet"].data[0]
    power = group["P"].data[0]
    
    # Compute magnitude and log-magnitude of S21
    magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
    log_mag_s21 = 20 * np.log10(magnitude_s21)
    
    return magnet, frequency, log_mag_s21, power

# FFT-based filtering
def adaptive_fft_filter(data, prominence_factor=0.5):
    fft_data = fft(data, axis=0)
    freqs = fftfreq(data.shape[0])
    power_spectrum = np.abs(fft_data)
    
    threshold = prominence_factor * np.max(power_spectrum, axis=0, keepdims=True)
    mask = power_spectrum < threshold
    fft_data *= mask
    
    filtered_data = np.real(ifft(fft_data, axis=0))
    return filtered_data

# Dictionary to store magnetic fields and their corresponding powers
magnetic_fields_and_powers = {}

# Iterate through all the TDMS files in the directory
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])

for file_name in tqdm(file_list, desc="Processing TDMS files"):
    file_path = os.path.join(folder_path, file_name)
    

    magnet, frequencies, log_magnitude_s21, power = process_tdms_file(file_path)
    filtered_log_magnitude_s21 = adaptive_fft_filter(log_magnitude_s21)
    
    # Find the minimum value of S21 and the corresponding power value
    min_value_index = np.unravel_index(np.argmin(filtered_log_magnitude_s21), filtered_log_magnitude_s21.shape)
    min_value = filtered_log_magnitude_s21[min_value_index]
    corresponding_power = min_value_index
    # corresponding_power = frequencies[min_value_index[0]] 

    # print(f"Magnetic Field: {magnet} T, Minimum S21: {min_value} dB, Power: {corresponding_power} dBm")
    if magnet == 0.0201:
        print(file_name)
    magnetic_fields_and_powers[magnet] = corresponding_power

# Plot the magnetic field vs power
magnetic_fields = list(magnetic_fields_and_powers.keys())
powers = list(magnetic_fields_and_powers.values())
print(magnetic_fields_and_powers)
idx = [1, 4, 6, 8, 10, 13, 16, 19]
x = [magnetic_fields[i] for i in idx]
y = [powers[i] for i in idx]

plt.figure(figsize=(8, 6))
plt.plot(x,y, marker='o', linestyle='-', color='b')
plt.xlabel('Magnetic Field (T)')
plt.ylabel('Power corresponding to minimum S21 (dBm)')
plt.title('Magnetic Field vs Power for Minimum S21')
plt.grid(True)
plt.show()
