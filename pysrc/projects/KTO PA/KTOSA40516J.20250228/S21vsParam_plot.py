import os
import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile
from tqdm import tqdm
from scipy.fftpack import fft, ifft, fftfreq
import tkinter as tk
from tkinter import filedialog, ttk

def get_parameters():
    root = tk.Tk()
    root.title("Data Analysis Parameters")
    
    # Folder selection
    folder_path = tk.StringVar()
    tk.Label(root, text="Data Folder:").pack(pady=5)
    tk.Entry(root, textvariable=folder_path).pack()
    tk.Button(root, text="Browse", command=lambda: folder_path.set(filedialog.askdirectory())).pack()

    # Parameter selection
    parameter = tk.StringVar(value="P")
    tk.Label(root, text="Parameter:").pack(pady=5)
    param_combo = ttk.Combobox(root, textvariable=parameter, values=["P", "Magnet", "Lockin Bias"])
    param_combo.pack()

    # Filter option
    filter_data = tk.BooleanVar(value=True)
    tk.Checkbutton(root, text="Apply FFT filtering", variable=filter_data).pack(pady=5)

    # Submit button
    result = {"folder_path": None, "parameter": None, "filter_data": None}
    def on_submit():
        result["folder_path"] = folder_path.get()
        result["parameter"] = parameter.get()
        result["filter_data"] = filter_data.get()
        root.destroy()
    
    tk.Button(root, text="Submit", command=on_submit).pack(pady=10)
    root.mainloop()
    
    return result["folder_path"], result["parameter"], result["filter_data"]

folder_path, parameter, filter_data = get_parameters()
if not folder_path:
    raise ValueError("No folder selected")
folder_path = folder_path + "/"


processed_data_file = folder_path + "./processed.npz"
if os.path.exists(processed_data_file):
    print("Loading processed data from file...")
    data = np.load(processed_data_file)
    frequencies = data["frequencies"]
    pars = data["pars"]
    log_magnitude_s21 = data["log_magnitude_s21"]
else:
    print("Processing raw TDMS files...")
    frequencies = None
    pars = []
    log_magnitude_s21 = []

    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith(".tdms")])
    for file_name in tqdm(file_list, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)
        tdms_file = TdmsFile.read(file_path)
        group = tdms_file["Data.000000"]
        frequency = group["frequency"].data
        re_s21 = group["ReS21"].data
        im_s21 = group["ImS21"].data

        magnitude_s21 = np.sqrt(re_s21**2 + im_s21**2)
        log_mag_s21 = 20 * np.log10(magnitude_s21)

        if frequencies is None:
            frequencies = frequency
        pars.append(group[parameter].data[0])
        log_magnitude_s21.append(log_mag_s21)

    pars = np.array(pars)
    log_magnitude_s21 = np.array(log_magnitude_s21)
    np.savez(processed_data_file, frequencies=frequencies, pars=pars, log_magnitude_s21=log_magnitude_s21)
    print(f"Processed data saved to {processed_data_file}")

# Adaptive FFT-based filtering

def adaptive_fft_filter(data, prominence_factor=0.05):
    fft_data = fft(data, axis=0)
    freqs = fftfreq(data.shape[0])
    power_spectrum = np.abs(fft_data)
    
    # Identify dominant noise frequencies
    threshold = prominence_factor * np.max(power_spectrum, axis=0, keepdims=True)
    mask = power_spectrum < threshold  # Keep only low-power components
    fft_data *= mask
    
    filtered_data = np.real(ifft(fft_data, axis=0))
    return filtered_data

filtered_log_magnitude_s21 = adaptive_fft_filter(log_magnitude_s21)

# Plot the filtered heatmap
fig, ax = plt.subplots(figsize=(8, 6))

plot_data = filtered_log_magnitude_s21 if filter_data else log_magnitude_s21
c = ax.pcolormesh(pars, frequencies, plot_data.T, cmap="plasma", shading="auto")
# ax.set_ylim(0.1e9, 1e9)
ax.set_xlabel(parameter)
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Log Magnitude of S21 (dB) Heatmap")
fig.colorbar(c, ax=ax, label="|S21| (dB)")

plt.show()


# from matplotlib.widgets import Slider

# # Create the plot
# fig, ax = plt.subplots(figsize=(12, 8))
# plt.subplots_adjust(bottom=0.25)  # Make room for sliders

# # Initial vmin and vmax
# vmin_init, vmax_init = -80, 0

# # Heatmap
# c = ax.pcolormesh(pars, frequencies, log_magnitude_s21.T, cmap="plasma", shading="auto", vmin=vmin_init, vmax=vmax_init)
# fig.colorbar(c, ax=ax, label="|S21| (dB)")

# ax.set_xlabel("B field")
# ax.set_ylabel("Frequency (Hz)")
# ax.set_title("Log Magnitude of S21 (dB) Heatmap")


# # Add sliders for vmin and vmax
# ax_vmin = plt.axes([0.2, 0.1, 0.65, 0.03])
# ax_vmax = plt.axes([0.2, 0.05, 0.65, 0.03])

# slider_vmin = Slider(ax_vmin, 'vmin', -120, 0, valinit=vmin_init)
# slider_vmax = Slider(ax_vmax, 'vmax', -120, 0, valinit=vmax_init)

# # Update function for sliders
# def update(val):
#     c.set_clim(vmin=slider_vmin.val, vmax=slider_vmax.val)
#     fig.canvas.draw_idle()

# slider_vmin.on_changed(update)
# slider_vmax.on_changed(update)

# plt.show()