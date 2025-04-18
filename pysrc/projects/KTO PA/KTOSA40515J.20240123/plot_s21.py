import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm

# Path to the folder containing tdms files
folder_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\MNK\SA40515J.20240123\11-Bsweep _70Vbg"
# Path to the temporary processed data file
processed_data_file = "./processed_s21_data_70Vbg.npz"

# Check if the processed data file exists
if os.path.exists(processed_data_file):
    print("Loading processed data from file...")
    data = np.load(processed_data_file)
    frequencies = data["frequencies"]
    b_fields = data["b_fields"]
    log_magnitude_s21 = data["log_magnitude_s21"]
else:
    print("Processing raw TDMS files...")
    # Initialize lists to store data
    frequencies = None
    b_fields = []
    log_magnitude_s21 = []

    # Loop through all tdms files in the folder with a progress bar
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])
    for file_name in tqdm(file_list, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)

        # Read the tdms file
        tdms_file = TdmsFile.read(file_path)

        # Access the group and channels
        group = tdms_file["Data.000000"]
        frequency = group["frequency"].data
        re_s21 = group["ReS21"].data
        im_s21 = group["ImS21"].data

        # Compute log magnitude of S21 in dB
        magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
        log_mag_s21 = 20 * np.log10(magnitude_s21)

        # Append data
        if frequencies is None:
            frequencies = frequency  # Frequency is the same for all files
        b_fields.append(group["Magnet"].data[0])  # Extract B field from file name
        log_magnitude_s21.append(log_mag_s21)

    # Convert lists to numpy arrays
    b_fields = np.array(b_fields)
    log_magnitude_s21 = np.array(log_magnitude_s21)

    # Save processed data to a file
    np.savez(processed_data_file, frequencies=frequencies, b_fields=b_fields, log_magnitude_s21=log_magnitude_s21)
    print(f"Processed data saved to {processed_data_file}")

# # Create the heatmap
# fig, ax = plt.subplots(figsize=(12, 8))
# c = ax.pcolormesh(b_fields, frequencies, log_magnitude_s21.T, cmap="viridis", shading="auto")

# # Labels, title, and colorbar
# ax.set_xlabel("B field")
# ax.set_ylabel("Frequency (Hz)")
# ax.set_title("Log Magnitude of S21 (dB) Heatmap")
# fig.colorbar(c, ax=ax, label="|S21| (dB)")

# plt.show()

from matplotlib.widgets import Slider

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.25)  # Make room for sliders

# Initial vmin and vmax
vmin_init, vmax_init = -80, 0

# Heatmap
c = ax.pcolormesh(b_fields, frequencies, log_magnitude_s21.T, cmap="plasma", shading="auto", vmin=vmin_init, vmax=vmax_init)
fig.colorbar(c, ax=ax, label="|S21| (dB)")

ax.set_xlabel("B field")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Log Magnitude of S21 (dB) Heatmap")


# Add sliders for vmin and vmax
ax_vmin = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_vmax = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_vmin = Slider(ax_vmin, 'vmin', -120, 0, valinit=vmin_init)
slider_vmax = Slider(ax_vmax, 'vmax', -120, 0, valinit=vmax_init)

# Update function for sliders
def update(val):
    c.set_clim(vmin=slider_vmin.val, vmax=slider_vmax.val)
    fig.canvas.draw_idle()

slider_vmin.on_changed(update)
slider_vmax.on_changed(update)

plt.show()
