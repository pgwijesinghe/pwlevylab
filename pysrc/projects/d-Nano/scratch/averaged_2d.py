#%%
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set the path to the folder containing the CSV files
folder_path = r"C:\Users\PubuduW\Desktop\avg_data"

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Initialize lists to store the x and device_PS values from each file
x_values = []
device_PS_values = []

# Iterate through all CSV files
for file_index, csv_file_name in enumerate(csv_files):
    file_path = os.path.join(folder_path, csv_file_name)
    
    # Read data from the CSV file using pandas
    df = pd.read_csv(file_path)
    
    # Assuming the CSV has columns 'Ch5_PS_x' and 'Ch5_PS_y' corresponding to 'x' and 'device_PS'
    x = df['Ch5_PS_x'].values
    device_PS = df['Ch5_PS_y'].values
    
    x_values.append(x[50:200])
    device_PS_values.append(device_PS[50:200])

# Convert lists to numpy arrays for easy handling in plotting
x_values = np.array([x for x in x_values])
device_PS_values = np.array([device_PS for device_PS in device_PS_values])

# Create a 2D plot: file_index vs x vs device_PS
plt.figure(figsize=(10, 6))

# Use imshow to create the intensity plot
plt.imshow(np.log(device_PS_values), aspect='auto', cmap='viridis', extent=[x_values.min(), x_values.max(), 0, len(csv_files)])

# Label axes
plt.colorbar(label="Device Power Spectral Intensity (device_PS)")
plt.xlabel('X')
plt.ylabel('File Index')
plt.title('Intensity Plot: File Index vs X vs Device_PS')

# Show the plot
plt.show()
