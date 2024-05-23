
"""
This is the first time I saw a SHG signal with the APD mounted in the far field.
In this data, the APD is showing a SHG signal only because it was saturated- leading to a non-linearity.
"""
import os
import nptdms
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from scipy.signal import find_peaks

# Set the path to the folder containing the TDMS files
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Pubudu's Data\SA40287.20231121.000088.tdms"

# Read Data
with nptdms.TdmsFile(file_path) as tdms_file:
    # Get the group and channel names for the two arrays you want to extract
    group1 = tdms_file["Data.000000"]
    apd_PS = group1["Ch8_PS_y"].data
    device_PS = group1["Ch2_PS_y"].data
    device_TD = group1["Ch2_y"].data
    apd_TD = group1["Ch8_y"].data
x=np.linspace(0, 25000, 5000)
tau = np.linspace(-0.1,0.1,len(device_TD))           

# Plot Power spectrums from Data
# plt.figure()
# plt.xlim(250,1000)
# plt.ylim(0,0.000000006)
# plt.plot(x,channel1.data, label="APD")
# plt.plot(x,channel2.data, label="LAO/STO",color='red')

# Plot Normalized TD Signals
plt.figure()
device_TD_norm = device_TD/np.max(device_TD)
apd_TD_norm = apd_TD/np.max(apd_TD)
plt.plot(tau, (apd_TD_norm),label="APD", color='blue')
plt.plot(tau, (device_TD_norm), label="LAO/STO",color='red')
plt.plot(tau, (apd_TD_norm-device_TD_norm), label="Difference",color='green')
plt.xlabel("Delay (ps))")
plt.ylabel("Signal (Normalized)")
plt.legend()
plt.show()

# Plot APD(tau) vs LAO/STO(tau)
plt.figure()
plt.plot(apd_TD_norm, device_TD_norm)
plt.xlabel("APD Signal (Normalized)")
plt.ylabel("LAO/STO Signal (Normalized)")

matplotlib.style.use('ggplot')
# Plot Power Spectrum from the TD Signals
x2=np.linspace(0, 50000, 10000)
power_spectrum_apd = np.abs(np.fft.fft(apd_TD_norm))
power_spectrum_device = np.abs(np.fft.fft(device_TD_norm))
power_spectrum_diff = np.abs(np.fft.fft(apd_TD_norm-device_TD_norm))
plt.figure()
plt.xlim(300,1500)
plt.ylim(0,250)
plt.plot(x2,power_spectrum_apd,label="APD", color='blue')
plt.plot(x2,power_spectrum_device,label="LAO/STO",color='red')
plt.plot(x2,power_spectrum_diff,label="Difference",color='green')
plt.xlabel("Frequency (THz)")
plt.ylabel("Power Spectrum")
plt.legend()
plt.show()

#integral Ratios
integral_fund_apd = np.trapz(power_spectrum_apd[70:92], x2[70:92]) # fundamental integral_apd
integral_fund_device = np.trapz(power_spectrum_device[70:92], x2[70:92]) # fundamental integral_device
integral_shg_apd = np.trapz(power_spectrum_apd[150:175], x2[150:175]) # 2nd harmonic integral_apd
integral_shg_device = np.trapz(power_spectrum_device[150:175], x2[150:175]) # 2nd harmonic integral_device

print(f"Ratios (APD, Device): {integral_fund_apd/integral_shg_apd} and {integral_fund_device/integral_shg_device}")




