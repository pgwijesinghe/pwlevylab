from nptdms import TdmsFile
import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
from tqdm import tqdm
matplotlib.style.use('ggplot')

# Define the folder containing the tdms files
tdms_folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287C.20241106\reps"

# Get all .tdms files in the folder
tdms_files = [f for f in os.listdir(tdms_folder_path) if f.endswith(".tdms")]

if not tdms_files:
    print("No '.tdms' files found.")
else:
    all_data = []
    print(f"Processing {len(tdms_files)} files...")

    # Loop through files with a progress bar
    for filename in tqdm(tdms_files, desc="Processing"):
        try:
            with TdmsFile(os.path.join(tdms_folder_path, filename)) as tdms_file:
                all_data.append(tdms_file["Data.000000"]["Ch7_y"].data)
        except Exception as e:
            print(f"Error with {filename}: {e}")

    td_x = np.linspace(-0.5, 0.5, len(all_data[0]))
    # Calculate and plot the average if data was collected
    if all_data:
        avg_data = np.mean(np.array(all_data), axis=0)
        plt.plot(td_x, avg_data)
        plt.title("Average Signal")
        plt.xlabel("Time Delay (ps)")
        plt.ylabel("Signal Amplitude")
        plt.show()
    else:
        print("No valid data to plot.")

# Save the average data to a CSV file
output_csv_path = os.path.join(tdms_folder_path, "average_signal.csv")
np.savetxt(output_csv_path, np.column_stack((td_x, avg_data)), delimiter=",", header="Time Delay (ps),Signal Amplitude", comments='')
print(f"Average signal data saved to {output_csv_path}")