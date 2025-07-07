import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.ndimage import median_filter
from scipy.fft import rfft, irfft, rfftfreq
import nptdms

# === Load TDMS Data ===
file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\10 - 20250604_CtrlExp\SA40653C.20250526.000377.tdms"

with nptdms.TdmsFile(file_path) as tdms_file:
    group = tdms_file["Data.000000"]
    delay = group["Delay"].data           # Delay in ps
    pc = group["Ch3_y"].data              # Photocurrent

# === Convert delay to seconds and compute sampling frequency ===
delay_s = delay * 1e-12
fs = 1 / np.mean(np.diff(delay_s))  # Hz

# === Plot FFT of raw signal ===
n = len(pc)
freq = rfftfreq(n, d=1/fs)
fft_mag = np.abs(rfft(pc))

plt.figure(figsize=(10, 4))
plt.semilogy(freq * 1e-12, fft_mag)
plt.title("FFT of Raw Signal")
plt.xlabel("Frequency [THz]")
plt.ylabel("Magnitude")
plt.grid(True)
plt.tight_layout()
plt.show()

# === Frequency-Domain Despiking ===
def fft_despike(signal, fs, threshold=8.0, window_size=9):
    """
    Removes spikes from the frequency domain using rolling MAD.
    """
    signal = np.asarray(signal, dtype=float)
    n = len(signal)
    freqs = rfftfreq(n, d=1/fs)
    spectrum = rfft(signal)
    mag = np.abs(spectrum)

    # Rolling MAD-based spike detection
    mag_med = median_filter(mag, size=window_size, mode='reflect')
    mad = median_filter(np.abs(mag - mag_med), size=window_size, mode='reflect')
    spike_mask = np.abs(mag - mag_med) > threshold * mad

    # Replace spike magnitudes with median, keep original phase
    cleaned_mag = np.copy(mag)
    cleaned_mag[spike_mask] = mag_med[spike_mask]
    spectrum_cleaned = cleaned_mag * np.exp(1j * np.angle(spectrum))

    return irfft(spectrum_cleaned, n=n)

# === Apply FFT Despiking and SG Smoothing ===
pc_fftcleaned = fft_despike(pc, fs=fs, threshold=8.0, window_size=9)
pc_filtered = savgol_filter(pc_fftcleaned, window_length=21, polyorder=3)

# === Plot Time-Domain Comparison ===
plt.figure(figsize=(12, 6))
plt.plot(delay, pc, label='Raw', alpha=0.4)
plt.plot(delay, pc_fftcleaned, label='FFT Despiked', linewidth=1.0)
plt.plot(delay, pc_filtered, label='FFT Despiked + SG Filtered', linewidth=1.5)
plt.xlabel("Delay [ps]")
plt.ylabel("Photocurrent [arb. u.]")
plt.title("THz Photocurrent Signal: Frequency-Domain Despiking + Smoothing")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
