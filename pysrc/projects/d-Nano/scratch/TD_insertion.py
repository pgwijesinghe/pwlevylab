#%%
import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np

folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250123\11 - 0203\TD vs Insertion"
tdms_files = [f for f in os.listdir(folder_path) if f.endswith('.tdms')]

# Initialize lists to store the x and device_PS values from each file
x_values = []
device_TD_values = []

# Iterate through all TDMS files
for file_index, tdms_file_name in enumerate(tdms_files):
    file_path = os.path.join(folder_path, tdms_file_name)
    
    # Read data from the TDMS file
    with nptdms.TdmsFile(file_path) as tdms_file:
        # Get the group and channel names for the data
        group = tdms_file["Data.000000"]
        x = group["Delay"].data
        device_TD = group["Ch6_y"].data

        x_values.append(x[0:100000])
        device_TD_values.append(device_TD[0:100000])
        
# Convert lists to numpy arrays for easy handling in plotting
x_values = np.array([x for x in x_values])
device_TD_value = np.array([device_TD for device_TD in device_TD_values])
print(len(x_values), len(device_TD_values))
#Create a 2D plot: file_index vs x vs device_PS
plt.figure(figsize=(10, 6))

# Use imshow to create the intensity plot
plt.imshow(device_TD_value, aspect='auto', cmap='plasma', extent=[x_values.min(), x_values.max(), 0, len(tdms_files)])

# Label axes
plt.colorbar(label="Device Power Spectral Intensity (device_PS)")
plt.xlabel('X')
plt.ylabel('File Index')
plt.title('Intensity Plot: File Index vs X vs Device_PS')

plt.show()

# %%
