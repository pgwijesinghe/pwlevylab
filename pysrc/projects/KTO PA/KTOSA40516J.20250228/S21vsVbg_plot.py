import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm
from scipy.fftpack import fft, ifft, fftfreq

# Path to the folder containing tdms files
folder_path = r"C:\Users\PubuduW\Desktop\11-Bg Sweep-20250304T183842Z-001\11-Bg Sweep"
# Path to the temporary processed data file
processed_data_file = folder_path + "./processed.npz"

# Check if the processed data file exists
if os.path.exists(processed_data_file):
    print("Loading processed data from file...")
    data = np.load(processed_data_file)
    frequencies = data["frequencies"]
    vg = data["vg"]
    log_magnitude_s21 = data["log_magnitude_s21"]
else:
    print("Processing raw TDMS files...")
    # Initialize lists to store data
    frequencies = None
    vg = []
    log_magnitude_s21 = []
    i=0
    # Loop through all tdms files in the folder with a progress bar
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])
    for file_name in tqdm(file_list, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)

        # Read the tdms file
        tdms_file = TdmsFile.read(file_path)

        # Access the group and channels
        group = tdms_file["Data.000000"]
        frequency = group["frequency"].data
        re_s21 = group["ReS21"].data
        im_s21 = group["ImS21"].data

        # Compute log magnitude of S21 in dB
        magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
        log_mag_s21 = 20 * np.log10(magnitude_s21)

        # Append data
        if frequencies is None:
            frequencies = frequency  # Frequency is the same for all files

        vg.append(group["Lockin Bias"].data[0])  # Extract Vg field from file name
        log_magnitude_s21.append(log_mag_s21)

    # Convert lists to numpy arrays
    vg = np.array(vg)
    log_magnitude_s21 = np.array(log_magnitude_s21)

    # Save processed data to a file
    np.savez(processed_data_file, frequencies=frequencies, vg=vg, log_magnitude_s21=log_magnitude_s21)
    print(f"Processed data saved to {processed_data_file}")

def adaptive_fft_filter(data, prominence_factor=0.005):
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

# Create the heatmap
fig, ax = plt.subplots(figsize=(12, 8))
filter_data = False
plot_data = filtered_log_magnitude_s21 if filter_data else log_magnitude_s21
c = ax.pcolormesh(vg, frequencies, plot_data.T, cmap="plasma", shading="auto", 
                #   vmin=-2, vmax=1
                )

# Labels, title, and colorbar
ax.set_xlabel("Vg (V)")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Log Magnitude of S21 (dB) Heatmap")
fig.colorbar(c, ax=ax, label="|S21| (dB)")

plt.show()
