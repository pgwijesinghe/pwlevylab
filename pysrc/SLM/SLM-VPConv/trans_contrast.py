import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter

vcalib_path = r"C:\Users\PubuduW\Desktop\Voltage Calib_20231129"

with open(os.path.join(vcalib_path, "Mask A.txt"), "r") as maskA, open(os.path.join(vcalib_path, "Mask B.txt"), "r") as maskB:
    dataA = np.genfromtxt(maskA, delimiter='\t')
    dataB = np.genfromtxt(maskB, delimiter='\t')

contrast_array = []
for px in range(640):
    data = dataA[:,px]
    contrast_array.append((max(data) - min(data))/max(data))

plt.plot(contrast_array)
plt.xlabel('Pixel')
plt.ylabel('Contrast')
plt.show()

