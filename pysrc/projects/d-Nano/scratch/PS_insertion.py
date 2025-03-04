#%%
import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np

# Set the path to the folder containing the TDMS files
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250123\02 - Delay vs Insertion"

# Get a list of all TDMS files in the folder
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

# Initialize lists to store the x and device_PS values from each file
x_values = []
device_PS_values = []

# Iterate through all TDMS files
for file_index, tdms_file_name in enumerate(tdms_files):
    file_path = os.path.join(folder_path, tdms_file_name)
    
    # Read data from the TDMS file
    with nptdms.TdmsFile(file_path) as tdms_file:
        # Get the group and channel names for the data
        group = tdms_file["Data.000000"]
        x = group["Ch5_PS_x"].data
        device_PS = group["Ch5_PS_y"].data
        
        # Slice the arrays to keep only values where x <= 1200
        slice_index = np.where(x <= 1200)[0][-1]  # Get the index of the last value where x <= 1200
        slice_index = 120
        x_values.append(x[20:slice_index + 1])
        device_PS_values.append(device_PS[20:slice_index + 1])

# Convert lists to numpy arrays for easy handling in plotting
x_values = np.array([x for x in x_values])
device_PS_values = np.array([device_PS for device_PS in device_PS_values])

# Create a 2D plot: file_index vs x vs device_PS
plt.figure(figsize=(10, 6))

# Use imshow to create the intensity plot
plt.imshow(np.log(device_PS_values), aspect='auto', cmap='viridis', extent=[x_values.min(), x_values.max(), 0, len(tdms_files)])

# Label axes
plt.colorbar(label="Device Power Spectral Intensity (device_PS)")
plt.xlabel('X')
plt.ylabel('File Index')
plt.title('Intensity Plot: File Index vs X vs Device_PS')

# Show the plot
plt.show()
