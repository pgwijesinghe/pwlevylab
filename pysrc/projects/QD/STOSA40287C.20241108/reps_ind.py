from nptdms import TdmsFile
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# Define the folder containing the tdms files
tdms_folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287C.20241106\reps"

# Get all .tdms files in the folder
tdms_files = [f for f in os.listdir(tdms_folder_path) if f.endswith(".tdms")]

if not tdms_files:
    print("No '.tdms' files found.")
else:
    print(f"Processing {len(tdms_files)} files...")
    
    # Create a single figure
    plt.figure(figsize=(10, 6))

    # Loop through files with a progress bar
    for filename in tqdm(tdms_files, desc="Processing"):
        try:
            # Read data from each file
            with TdmsFile(os.path.join(tdms_folder_path, filename)) as tdms_file:
                data = tdms_file["Data.000000"]["Ch7_y"].data
            
            # Plot the data on the same figure
            plt.plot(data, label=filename)
        except Exception as e:
            print(f"Error with {filename}: {e}")

    # Customize the plot
    plt.title("Signals from TDMS Files")
    plt.xlabel("Time Points")
    plt.ylabel("Signal Amplitude")
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Place legend outside the plot
    plt.tight_layout()
    plt.show()
