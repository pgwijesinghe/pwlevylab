import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Define the folder containing your text files.
# IMPORTANT: Please replace this path with the actual path to your data folder.
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\21 - Bias vs PC vs Insertion_20K"

# --- Data Collection and Preprocessing ---
# This list will store all raw data points across all files to determine the global range of insertion values.
# Photocurrent data will be collected, but then normalized per bias curve for the imshow plot.
all_insertion_raw = []
# This list will store processed data for each file, including bias, insertion, and photocurrent arrays.
file_data_list = [] 

print(f"Attempting to scan folder: {folder_path}")
try:
    # Iterate over each file in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file is a .txt file and contains 'Bias=' in its name
        if filename.endswith('.txt') and 'Bias=' in filename:
            try:
                # Extract the Bias value from the filename.
                # It assumes a format like '..._Bias=X.X.txt'.
                # Splits by 'Bias=', takes the second part, then splits by '.txt' and takes the first part.
                bias_value_str = filename.split('Bias=')[1].split('.txt')[0]
                bias_value = float(bias_value_str) # Convert the extracted string to a float

                file_path = os.path.join(folder_path, filename)
                
                insertion_values = []
                photocurrent_values = []
                
                # Open and read the data from the current file
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                
                # Parse each line to extract insertion and photocurrent values
                for line in lines:
                    columns = line.split() # Split the line by whitespace
                    if len(columns) >= 2: # Ensure there are at least two columns
                        try:
                            insertion_val = float(columns[0])
                            photocurrent_val = float(columns[1])
                            insertion_values.append(insertion_val)
                            photocurrent_values.append(photocurrent_val)
                            
                            # Add raw insertion values to global list for overall range calculation
                            all_insertion_raw.append(insertion_val)
                        except ValueError:
                            # Skip lines if data conversion to float fails
                            continue
                
                # Only add file data to the list if valid insertion and photocurrent values were found
                if insertion_values and photocurrent_values:
                    file_data_list.append({
                        'bias': bias_value,
                        'insertion': np.array(insertion_values), # Convert to NumPy array for easier manipulation
                        'photocurrent': np.array(photocurrent_values)
                    })
                else:
                    print(f"Warning: No valid data points found in {filename}. Skipping this file.")

            except (IndexError, ValueError) as e:
                # Catch errors during filename parsing or data conversion
                print(f"Could not parse filename or data for {filename}. Error: {e}. Skipping this file.")
                continue
except FileNotFoundError:
    print(f"Error: The specified folder was not found at '{folder_path}'. Please verify the 'folder_path'.")
    exit() # Exit the script if the folder doesn't exist

# Check if any data was processed from the files
if not file_data_list:
    print("No valid data files found or processed. Please ensure the folder contains relevant .txt files and the naming convention is correct. Exiting.")
    exit()

# --- Global Range for Insertion and Local Normalization for Photocurrent ---
# Calculate global minimum and maximum for all insertion values (for x-axis range).
min_insertion_global = np.min(all_insertion_raw) if all_insertion_raw else 0
max_insertion_global = np.max(all_insertion_raw) if all_insertion_raw else 1

# Define a helper function for Min-Max normalization
def normalize_array_local(arr):
    """Normalizes a numpy array to the range [0, 1] based on its own min/max."""
    min_val = np.min(arr)
    max_val = np.max(arr)
    if (max_val - min_val) == 0:
        return np.full_like(arr, 0.5) # Return 0.5 if all values are the same
    return (arr - min_val) / (max_val - min_val)

# --- Prepare Axes for imshow Plot ---
# Y-axis data: Get all unique bias values and sort them.
bias_labels = sorted(list(set(d['bias'] for d in file_data_list)))
num_bias_points = len(bias_labels)

# X-axis data: Create a common, dense grid of RAW insertion values.
# This grid will serve as the x-axis for the imshow plot.
# Using 200 points to create a smooth representation.
common_insertion_grid = np.linspace(
    min_insertion_global,
    max_insertion_global,
    200
)
num_insertion_points = len(common_insertion_grid)

# --- Populate the Z-data Matrix (Photocurrent for color intensity) ---
# Initialize the 2D array that imshow will display.
# Fill with NaN (Not a Number) initially to represent areas where no data exists.
Z_data = np.full((num_bias_points, num_insertion_points), np.nan)

# Create a mapping from bias value to its row index in the Z_data matrix
bias_to_row_index = {bias: i for i, bias in enumerate(bias_labels)}

# Iterate through each file's processed data
for data_entry in file_data_list:
    bias_val = data_entry['bias']
    # Use raw insertion values for interpolation
    insertion_current_file = data_entry['insertion'] 
    photocurrent_current_file = data_entry['photocurrent']

    # Ensure there are enough data points for interpolation (at least 2 for 'linear' kind)
    if len(insertion_current_file) < 2:
        print(f"Warning: Not enough data points ({len(insertion_current_file)}) for interpolation for Bias={bias_val}. Skipping this data slice.")
        continue

    # --- LOCAL NORMALIZATION FOR THE IMAGESHOW PLOT'S Z-DATA ---
    # Normalize the photocurrent values from the current file locally (per bias curve).
    # This ensures each horizontal slice (row) in the imshow plot is scaled 0-1.
    normalized_photocurrent_current_file_local = normalize_array_local(photocurrent_current_file)

    try:
        # Create an interpolation function using scipy.interpolate.interp1d
        # The x-values for interpolation are the raw insertion values.
        f_interp = interp1d(
            insertion_current_file,
            normalized_photocurrent_current_file_local, # Use locally normalized data for imshow
            kind='linear',
            fill_value='extrapolate'
        )
        
        # Use the interpolation function to get photocurrent values on the common insertion grid
        # This grid also uses raw insertion values.
        photocurrent_interpolated = f_interp(common_insertion_grid)
        
        # Find the correct row in Z_data for the current bias value
        row_index = bias_to_row_index[bias_val]
        # Assign the interpolated photocurrent values to that row
        Z_data[row_index, :] = photocurrent_interpolated
    except ValueError as e:
        print(f"Error interpolating data for Bias={bias_val}. Error: {e}. Skipping this bias level.")
        continue

# --- Plotting ---
plt.figure(figsize=(10, 8)) # Create a figure

# Main imshow plot
# The extent sets the x and y limits for the plot.
# x-limits are min/max of global insertion.
# y-limits are min/max of bias labels.
c = plt.imshow(Z_data, aspect='auto', origin='lower', extent=[min_insertion_global, max_insertion_global, min(bias_labels), max(bias_labels)], cmap='plasma')

plt.title('Normalized Photocurrent Intensity')
plt.xlabel('Insertion')
plt.ylabel('Bias Value')

# Update colorbar label to reflect local normalization per bias curve
plt.colorbar(c, label='Normalized Photocurrent (Local per Bias)')

# Removed plt.yticks(bias_labels) to allow auto-adjustment of the y-axis
plt.grid(True, linestyle='--', alpha=0.7)

plt.show()
