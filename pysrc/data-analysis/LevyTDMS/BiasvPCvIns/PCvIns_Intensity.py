import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Define the folder containing your text files.
# IMPORTANT: Please replace this path with the actual path to your data folder.
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\21 - Bias vs PC vs Insertion_20K"

# --- Data Collection and Preprocessing ---
# These lists will store all raw data points across all files
all_insertion_raw = []
all_photocurrent_raw = []
# This list will store processed data for each file, including bias, insertion, and photocurrent arrays
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
                            
                            # Add raw values to global lists for overall range calculation
                            all_insertion_raw.append(insertion_val)
                            all_photocurrent_raw.append(photocurrent_val)
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

# --- Global Range for Insertion and Normalization for Photocurrent ---
# Calculate global minimum and maximum for all insertion values (for x-axis range).
min_insertion_global = np.min(all_insertion_raw) if all_insertion_raw else 0
max_insertion_global = np.max(all_insertion_raw) if all_insertion_raw else 1

# Calculate global minimum and maximum for all photocurrent values (for z-axis normalization).
min_photocurrent_global = np.min(all_photocurrent_raw) if all_photocurrent_raw else 0
max_photocurrent_global = np.max(all_photocurrent_raw) if all_photocurrent_raw else 1

# Define a helper function for Min-Max normalization (ONLY used for photocurrent now)
def normalize_value(value, min_val, max_val):
    if (max_val - min_val) == 0:
        # Avoid division by zero if all values are the same; return 0.5 (middle of 0-1 range)
        return 0.5 
    return (value - min_val) / (max_val - min_val)

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

    # Normalize the photocurrent values from the current file using GLOBAL min/max.
    # Insertion values are NOT normalized here.
    normalized_photocurrent_current_file = np.array([normalize_value(x, min_photocurrent_global, max_photocurrent_global) for x in photocurrent_current_file])

    try:
        # Create an interpolation function using scipy.interpolate.interp1d
        # The x-values for interpolation are now the raw insertion values.
        f_interp = interp1d(
            insertion_current_file,
            normalized_photocurrent_current_file,
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

# --- Interactive Plotting Setup ---
fig = plt.figure(figsize=(15, 10)) # Create a figure to hold multiple subplots

# Main imshow plot (top-left)
ax_main = fig.add_subplot(221) # 2 rows, 2 columns, 1st subplot
c = ax_main.imshow(Z_data, aspect='auto', origin='lower', extent=[min_insertion_global, max_insertion_global, min(bias_labels), max(bias_labels)], cmap='viridis')
ax_main.set_title('Normalized Photocurrent Intensity (Click for Line Cuts)')
ax_main.set_xlabel('Insertion')
ax_main.set_ylabel('Bias Value')
fig.colorbar(c, ax=ax_main, label='Normalized Photocurrent')
ax_main.set_yticks(bias_labels)
ax_main.grid(True, linestyle='--', alpha=0.7)

# Line cut subplots
ax_h_cut = fig.add_subplot(223) # Bottom-left for horizontal cut
ax_h_cut.set_title('Horizontal Line Cut (Photocurrent vs Insertion)')
ax_h_cut.set_xlabel('Insertion')
ax_h_cut.set_ylabel('Normalized Photocurrent')
ax_h_cut.grid(True, linestyle='--', alpha=0.7)

ax_v_cut = fig.add_subplot(222) # Top-right for vertical cut
ax_v_cut.set_title('Vertical Line Cut (Photocurrent vs Bias)')
ax_v_cut.set_xlabel('Bias Value')
ax_v_cut.set_ylabel('Normalized Photocurrent')
ax_v_cut.grid(True, linestyle='--', alpha=0.7)

# Store the line objects for updating (horizontal and vertical lines on main plot)
h_line = None
v_line = None

def onclick(event):
    global h_line, v_line # Declare global to modify them

    # Ensure the click was on the main imshow plot and within its data limits
    if event.inaxes == ax_main and event.xdata is not None and event.ydata is not None:
        clicked_insertion = event.xdata
        clicked_bias = event.ydata

        # --- Update Main Plot with Click Lines ---
        # Clear previous lines if they exist
        if h_line:
            h_line.remove()
        if v_line:
            v_line.remove()

        # Add horizontal and vertical lines at the click position on the main plot
        h_line = ax_main.axhline(clicked_bias, color='r', linestyle='--', alpha=0.8)
        v_line = ax_main.axvline(clicked_insertion, color='r', linestyle='--', alpha=0.8)

        # --- Horizontal Line Cut (Photocurrent vs. Insertion at clicked Bias) ---
        ax_h_cut.clear() # Clear previous plot
        ax_h_cut.set_title(f'Horizontal Line Cut (Photocurrent vs Insertion) @ Bias={clicked_bias:.2f}')
        ax_h_cut.set_xlabel('Insertion')
        ax_h_cut.set_ylabel('Normalized Photocurrent')
        ax_h_cut.grid(True, linestyle='--', alpha=0.7)

        # Find the closest bias value in our data to the clicked bias
        closest_bias_idx = np.abs(np.array(bias_labels) - clicked_bias).argmin()
        selected_bias_for_cut = bias_labels[closest_bias_idx]
        
        # Get the corresponding row of interpolated photocurrent data
        horizontal_cut_data = Z_data[closest_bias_idx, :]
        ax_h_cut.plot(common_insertion_grid, horizontal_cut_data, color='blue')
        ax_h_cut.axvline(clicked_insertion, color='red', linestyle=':', alpha=0.7) # Mark clicked insertion

        # --- Vertical Line Cut (Photocurrent vs. Bias at clicked Insertion) ---
        ax_v_cut.clear() # Clear previous plot
        ax_v_cut.set_title(f'Vertical Line Cut (Photocurrent vs Bias) @ Insertion={clicked_insertion:.2f}')
        ax_v_cut.set_xlabel('Bias Value')
        ax_v_cut.set_ylabel('Normalized Photocurrent')
        ax_v_cut.grid(True, linestyle='--', alpha=0.7)
        ax_v_cut.axhline(clicked_bias, color='red', linestyle=':', alpha=0.7) # Mark clicked bias

        # Get the corresponding column of interpolated photocurrent data
        # Find the index of the clicked insertion on the common_insertion_grid
        closest_insertion_idx = np.abs(common_insertion_grid - clicked_insertion).argmin()
        vertical_cut_data = Z_data[:, closest_insertion_idx]
        ax_v_cut.plot(bias_labels, vertical_cut_data, color='green')

        # Adjust layout and redraw the figure
        fig.tight_layout()
        fig.canvas.draw_idle()

# Connect the click event to our function
fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

