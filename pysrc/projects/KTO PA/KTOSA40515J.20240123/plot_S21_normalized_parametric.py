import numpy as np
import matplotlib.pyplot as plt
from nptdms import TdmsFile

data_folder = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\MNK\SA40515J.20240123\04-Sweep B S21"

file_idx = [280, 190]  # index for low Bfield file and high Bfield file

# Load the data
tdms_file_Bl = TdmsFile(data_folder + f"\\SA40515J.20240123.000{file_idx[0]}.tdms")  
tdms_file_Bh = TdmsFile(data_folder + f"\\SA40515J.20240123.000{file_idx[1]}.tdms")

print(f'Analyzing for {tdms_file_Bl["Data.000000"]["Magnet"].data[0]} T normalized with {tdms_file_Bh["Data.000000"]["Magnet"].data[0]} T' )

# Extract frequency and S21 data
frequencies = tdms_file_Bl["Data.000000"]["frequency"].data
Re_S21_Bl, Im_S21_Bl = tdms_file_Bl["Data.000000"]["ReS21"].data, tdms_file_Bl["Data.000000"]["ImS21"].data
Re_S21_Bh, Im_S21_Bh = tdms_file_Bh["Data.000000"]["ReS21"].data, tdms_file_Bh["Data.000000"]["ImS21"].data

# Normalize the S21 data at high field
S21_normalized = (Re_S21_Bl + 1j * Im_S21_Bl) / (Re_S21_Bh + 1j * Im_S21_Bh)

# Convert to polar coordinates (magnitude and phase)
magnitude_S21 = np.abs(S21_normalized)
phase_S21 = np.angle(S21_normalized)

def plot_s21_complex_normalized(type='polar'):
    if type == 'polar':
        # Create a polar plot
        plt.figure(figsize=(8, 6))
        plt.subplot(111, projection='polar')
        plt.scatter(phase_S21, magnitude_S21, c=frequencies, cmap='plasma', edgecolors='none', s=5)
        plt.colorbar(label='Frequency')
        plt.title('S21(f) in Polar Coordinates with High Field Normalization')
        plt.show()
    elif type == 'complex':
        # Plot the parametric plot: Re(S21) vs Im(S21)
        plt.figure(figsize=(8, 6))
        plt.scatter(np.real(S21_normalized), np.imag(S21_normalized), c=frequencies, cmap='plasma', edgecolors='none', s=5)
        plt.colorbar(label='Frequency')
        plt.xlabel('Re(S21)')
        plt.ylabel('Im(S21)')
        plt.title('S21(f) on Complex Plane with High Field Normalization')
        plt.grid(True)
        plt.show()
    else:
        raise ValueError('Invalid plot type. Use "polar" or "complex".')

plot_s21_complex_normalized(type='polar')
