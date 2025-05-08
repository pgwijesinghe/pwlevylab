import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
from nptdms import TdmsFile

file_idx = [277, 190]  # Index for low Bfield file and high Bfield file

# Load the TDMS files
tdms_file_Bl = TdmsFile(f"G:\\.shortcut-targets-by-id\\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\\ansom\\Data\\MNK\\SA40515J.20240123\\04-Sweep B S21\\SA40515J.20240123.000{file_idx[0]}.tdms")  
tdms_file_Bh = TdmsFile(f"G:\\.shortcut-targets-by-id\\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\\ansom\\Data\\MNK\\SA40515J.20240123\\04-Sweep B S21\\SA40515J.20240123.000{file_idx[1]}.tdms") 

print(tdms_file_Bl["Data.000000"]["Magnet"].data[0])


# # Extract data from TDMS files
# frequencies = tdms_file_Bl["Data.000000"]["frequency"].data
# Re_S21_Bl = tdms_file_Bl["Data.000000"]["ReS21"].data
# Im_S21_Bl = tdms_file_Bl["Data.000000"]["ImS21"].data
# Re_S21_Bh = tdms_file_Bh["Data.000000"]["ReS21"].data
# Im_S21_Bh = tdms_file_Bh["Data.000000"]["ImS21"].data

# # Normalize the S21 data at high field
# S21_normalized = (Re_S21_Bl + 1j * Im_S21_Bl) / (Re_S21_Bh + 1j * Im_S21_Bh)

# # Extract the real and imaginary parts
# real_S21 = np.real(S21_normalized)
# imag_S21 = np.imag(S21_normalized)

# # Normalize the frequency for color mapping (0 -> red, 1 -> blue)
# freq_norm = (frequencies - frequencies.min()) / (frequencies.max() - frequencies.min())

# # Create segments for the line plot (pairs of consecutive points)
# segments = []
# for i in range(len(real_S21) - 1):
#     segment = [[real_S21[i], imag_S21[i]], [real_S21[i + 1], imag_S21[i + 1]]]
#     segments.append(segment)

# # Create a LineCollection
# lc = LineCollection(segments, cmap='plasma', array=freq_norm, linewidth=2)

# # Plot
# fig, ax = plt.subplots(figsize=(8, 6))
# ax.add_collection(lc)
# ax.set_xlim([min(real_S21), max(real_S21)])
# ax.set_ylim([min(imag_S21), max(imag_S21)])

# # Add a colorbar
# plt.colorbar(lc, label='Frequency')

# # Set labels and title
# ax.set_xlabel('Re(S21)')
# ax.set_ylabel('Im(S21)')
# ax.set_title('S21(f) on Complex Plane with High Field Normalization (Continuous Line)')

# plt.grid(True)
# plt.show()
