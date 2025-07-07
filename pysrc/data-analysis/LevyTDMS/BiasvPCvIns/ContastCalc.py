import os
import matplotlib.pyplot as plt

folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\21 - Bias vs PC vs Insertion_20K"

bias_arr = []
contrast_arr = []

for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        # Extract bias as a float for better plotting
        bias_value = float(filename.split('Bias=')[1].split('.txt')[0])
        bias_arr.append(bias_value)
        
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        insertion_values = []
        photocurrent_values = []
        for line in lines:
            columns = line.split()
            if len(columns) >= 2:
                try:
                    insertion_values.append(float(columns[0]))
                    photocurrent_values.append(float(columns[1]))
                except ValueError:
                    continue  # Skip invalid data
        
        contrast_arr.append((max(photocurrent_values) - min(photocurrent_values)) / min(photocurrent_values) * 100)

# Plotting
plt.plot(bias_arr, contrast_arr)
plt.title('Photocurrent vs Insertion for different Bias values')
plt.xlabel('Bias (V)')
plt.ylabel('Contrast (%)')
plt.grid(True)
plt.tight_layout()

# Adjust x-axis ticks for better readability (Optional)
plt.xticks(rotation=45)

# Show the plot
plt.show()
