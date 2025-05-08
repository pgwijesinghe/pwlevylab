import os
import nptdms
import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.signal import detrend

# === Load TDMS File ===
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40663G.20250403\Ins_TD_P_20250414\SA40663G.20250403.000070.tdms"
with nptdms.TdmsFile(file_path) as tdms_file:
    group = tdms_file["Data.000000"]
    delay = group["Delay"].data
    pv = group["Ch2_y"].data

plt.plot(delay, pv)


# === Detrend signal to remove DC offset and slow drift ===
pv_detrended = detrend(pv, type='linear')

# === Optional: Crop first few points if early spike dominates ===
crop = True
crop_points = 100  # adjust as needed
if crop:
    delay = delay[crop_points:]
    pv_detrended = pv_detrended[crop_points:]

# === Time step between delay points ===
dt = np.mean(np.diff(delay))  # in ps, so freq will be in THz

# === Define scales for CWT ===
scales = np.arange(1, 256)

# === Compute CWT ===
wavelet = pywt.ContinuousWavelet('morl')
coefficients, _ = pywt.cwt(pv_detrended, scales, wavelet, sampling_period=dt)

# === Convert scales to frequencies (e.g., in THz if delay is in ps) ===
central_freq = pywt.central_frequency(wavelet)
frequencies = central_freq / (scales * dt)

# === Clip color scale to 99th percentile to avoid spike dominance ===
magnitude = np.abs(coefficients)
vmax = np.percentile(magnitude, 99)

# === Plot ===
plt.figure(figsize=(12, 6))
plt.imshow(magnitude, extent=[delay[0], delay[-1], frequencies[-1], frequencies[0]],
           cmap='jet', aspect='auto', vmax=vmax)
plt.colorbar(label='Magnitude')
plt.xlabel('Delay (ps)')
plt.ylabel('Frequency (THz)')
plt.title('CWT of PV Signal (Frequency Domain)')
plt.tight_layout()
plt.show()
