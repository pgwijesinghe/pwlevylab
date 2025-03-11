import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm
from scipy.fftpack import fft, ifft, fftfreq

# Path to the folder containing tdms files
folder_path = r"C:\Users\PubuduW\Desktop\SA40516T.20240228\02-B sweep"
# Path to the temporary processed data file
processed_data_file = folder_path + "./processed.npz"

# Check if the processed data file exists
if os.path.exists(processed_data_file):
    print("Loading processed data from file...")
    data = np.load(processed_data_file)
    frequencies = data["frequencies"]
    b_fields = data["b_fields"]
    log_magnitude_s21 = data["log_magnitude_s21"]
else:
    print("Processing raw TDMS files...")
    frequencies = None
    b_fields = []
    log_magnitude_s21 = []

    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])
    for file_name in tqdm(file_list, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)
        tdms_file = TdmsFile.read(file_path)
        group = tdms_file["Data.000000"]
        frequency = group["frequency"].data
        re_s21 = group["ReS21"].data
        im_s21 = group["ImS21"].data

        magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
        log_mag_s21 = 20 * np.log10(magnitude_s21)

        if frequencies is None:
            frequencies = frequency
        b_fields.append(group["Magnet"].data[0])
        log_magnitude_s21.append(log_mag_s21)

    b_fields = np.array(b_fields)
    log_magnitude_s21 = np.array(log_magnitude_s21)
    np.savez(processed_data_file, frequencies=frequencies, b_fields=b_fields, log_magnitude_s21=log_magnitude_s21)
    print(f"Processed data saved to {processed_data_file}")

# Adaptive FFT-based filtering

def adaptive_fft_filter(data, prominence_factor=0.05):
    fft_data = fft(data, axis=0)
    freqs = fftfreq(data.shape[0])
    power_spectrum = np.abs(fft_data)
    
    # Identify dominant noise frequencies
    threshold = prominence_factor * np.max(power_spectrum, axis=0, keepdims=True)
    mask = power_spectrum < threshold  # Keep only low-power components
    fft_data *= mask
    
    filtered_data = np.real(ifft(fft_data, axis=0))
    return filtered_data

filtered_log_magnitude_s21 = adaptive_fft_filter(log_magnitude_s21)

# Plot the filtered heatmap
fig, ax = plt.subplots(figsize=(8, 6))
c = ax.pcolormesh(b_fields, frequencies, filtered_log_magnitude_s21.T, cmap="copper", shading="auto") 
ax.set_xlabel("B field")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Adaptively Filtered Log Magnitude of S21 (dB) Heatmap")
fig.colorbar(c, ax=ax, label="|S21| (dB)")

plt.show()
