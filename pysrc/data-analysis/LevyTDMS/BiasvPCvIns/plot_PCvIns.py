import os
import matplotlib.pyplot as plt

# Define the folder containing your text files
folder_path = r'G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\18 - Bias vs PC vs Insertion_FineScan'

# Create a figure for plotting
plt.figure(figsize=(10, 6))

# Loop over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Extract Bias value from the filename
        bias_value = filename.split('_')[1].split('=')[1]
        
        file_path = os.path.join(folder_path, filename)
        
        # Open the file and read line by line
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Initialize lists to store extracted data
        insertion_values = []
        photocurrent_values = []
        
        # Iterate over each line in the file
        for line in lines:
            columns = line.split()
            if len(columns) >= 2:
                try:
                    # Convert to float and append
                    insertion_values.append(float(columns[0]))
                    photocurrent_values.append(float(columns[1]))
                except ValueError:
                    continue  # Skip lines with invalid data

        # Plot the data
        plt.plot(insertion_values, photocurrent_values, label=f'Bias={bias_value}')

# Customize the plot
plt.title('Photocurrent vs Insertion for different Bias values')
plt.xlabel('Insertion (mm)')
plt.ylabel('Photocurrent (A)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
