import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm

# Path to the folder containing tdms files
folder_path = r"C:\Users\pubud\Desktop\ktopa_dataanalysis\40516.0228\09-Power Sweep (0.002T)"
# Path to the temporary processed data file
processed_data_file = folder_path + "./processed2.npz"

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
        b_fields.append(group["P"].data[0])
        log_magnitude_s21.append(log_mag_s21)

    b_fields = np.array(b_fields)
    log_magnitude_s21 = np.array(log_magnitude_s21)
    np.savez(processed_data_file, frequencies=frequencies, b_fields=b_fields, log_magnitude_s21=log_magnitude_s21)
    print(f"Processed data saved to {processed_data_file}")

# Select a specific magnetic field value (e.g., 0.5 T)
selected_b_field = -12  # Change this to the desired B field value

# Find the index of the specified B field value
print(b_fields)
b_field_index = np.where(b_fields == selected_b_field)[0]

if len(b_field_index) > 0:
    # Retrieve the corresponding log magnitude S21 for the selected B field
    selected_log_magnitude_s21 = log_magnitude_s21[b_field_index[0]]

    # Plot S21 vs Frequency for the selected B field
    plt.figure(figsize=(8, 6))
    plt.plot(frequencies, selected_log_magnitude_s21, label=f"Power = {selected_b_field} dBm", color='b')
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Log Magnitude of S21 (dB)")
    plt.title(f"S21 vs Frequency for Power = {selected_b_field} dBm")
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print(f"B field value {selected_b_field} T not found in the data.")
