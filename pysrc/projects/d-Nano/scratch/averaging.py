import nptdms
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# Set the path to the folder containing the TDMS files
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250123\07 - Delay vs Insertion\07 - Insertion_25"
file_extension = ".tdms"

# Initialize lists to store the data
device_TD_all = []
device_PS_all = []
delay_all = []
x_all = []

# Get a list of all TDMS files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith(file_extension)]

# Loop through each file to read the data
for file in files:
    file_path = os.path.join(folder_path, file)
    
    with nptdms.TdmsFile(file_path) as tdms_file:
        # Get the group and channel names for the two arrays you want to extract
        group = tdms_file["Data.000000"]
        delay = group["Delay"].data
        device_TD = group["Ch5_y"].data
        x = group["Ch5_PS_x"].data
        device_PS = group["Ch5_PS_y"].data
        
        # Store the data from each file
        delay_all.append(delay)
        device_TD_all.append(device_TD)
        device_PS_all.append(device_PS)
        x_all.append(x)

# Convert the lists into numpy arrays (to make sure they align)
delay_all = np.array(delay_all)
device_TD_all = np.array(device_TD_all)
device_PS_all = np.array(device_PS_all)

# Average the data across all files
avg_device_TD = np.mean(device_TD_all, axis=0)
avg_device_PS = np.mean(device_PS_all, axis=0)

# Assuming the x values and delay are the same for all files, we'll just use the first file's x and delay
x_avg = x_all[0]  # Assuming x values are consistent across files
delay_avg = delay_all[0]  # Assuming delay values are consistent across files

# Create a pandas DataFrame with the averaged data
df = pd.DataFrame({
    # 'Delay': delay_avg,
    # 'Ch5_y': avg_device_TD,
    'Ch5_PS_x': x_avg,
    'Ch5_PS_y': avg_device_PS
})

# Specify the path for the new CSV file
new_file_path = os.path.join(folder_path, 'averaged_data.csv')

# Save the DataFrame to a CSV file
df.to_csv(new_file_path, index=False)

print(f"New CSV file created at: {new_file_path}")

# Optionally, plot the averaged data
plt.figure()
plt.plot(x_avg, np.log(avg_device_PS))
plt.xlim(0, 1200)
plt.title("Averaged Device PS Data")
plt.show()
