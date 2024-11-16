'''
Varying the intensity with time with the HWP, measuring APD response and the device response and plotting them one vs. another
Parametric Plot
APD(t) vs LAO/STO(t)
'''
import os
import nptdms
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.signal import find_peaks

# Set the path to the folder containing the TDMS files
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\99\SA40287.20231121.000115.tdms"
# file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40287.20231121\Int Dependence\SA40287.20231121.000016.tdms"108

# Read Data
with nptdms.TdmsFile(file_path) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group1 = tdms_file["Data.000000"]
    PS_x = group1["Ch8_PS_x"].data
    TD_x = group1["Ch8_x"].data
    apd_PS = group1["Ch8_PS_y"].data
    device_PS = group1["Ch2_PS_y"].data
    device_TD = group1["Ch2_y"].data
    apd_TD = group1["Ch8_y"].data

delay_range = [-0.05, -0.046] # delay range for the time domain signals in ps
x = np.linspace(0, max(PS_x), len(PS_x)) #x-axis for the power spectrum
tau = np.linspace(delay_range[0],delay_range[1],len(TD_x)) #x-axis for the time domain signals          

# normalize the signals
device_TD_norm = device_TD/np.max(device_TD)
apd_TD_norm = apd_TD/np.max(apd_TD)

#smoothen the signals
from scipy.signal import savgol_filter
device_TD_norm_filtered = savgol_filter(device_TD_norm, 1000, 3)
apd_TD_norm_filtered = savgol_filter(apd_TD_norm, 1000, 3)

#plot the smoothened signals
plt.figure()
plt.plot(device_TD_norm_filtered, apd_TD_norm_filtered, color='blue')
plt.xlabel("LAO/STO Signal (Normalized)")
plt.ylabel("APD Signal (Normalized)")
plt.show()

# plot the normalized signals
plt.figure()
plt.plot(tau, device_TD_norm, color='blue',label="LAO/STO")
plt.plot(tau, apd_TD_norm, color='red',label="APD")
plt.xlabel("Delay (ps))")
plt.ylabel("Signal (Normalized)")
plt.title("Normalized Signals")
plt.legend()
plt.show()

#plot the power spectrum
power_spectrum_apd = np.abs(np.fft.fft(apd_TD_norm)) # power spectrum from TD signal
power_spectrum_device = np.abs(np.fft.fft(device_TD_norm))
plt.figure()
plt.plot(PS_x, np.log(device_PS), label="LAO/STO",color='red')
plt.plot(PS_x, np.log(apd_PS), label="APD", color='blue')
# plt.xlim(0, 5000)
plt.ylim(-40, -10)
plt.ylabel("Log(Intensity)")
plt.xlabel("Frequency (THz)")
plt.legend()
plt.show()
