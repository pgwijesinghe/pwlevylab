import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks, savgol_filter

# set the path to the voltage calibration data
vcalib_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Pubudu's Data\Voltage Calib_20231129"

# read the data
with open(os.path.join(vcalib_path, "Mask A.txt"), "r") as maskA, open(os.path.join(vcalib_path, "Mask B.txt"), "r") as maskB:
    dataA = np.genfromtxt(maskA, delimiter='\t')
    dataB = np.genfromtxt(maskB, delimiter='\t')

#plot the data (heatmaps)
fig,ax = plt.subplots(1,2)
ax[0].imshow(dataA, cmap='viridis')
ax[0].set_title('Mask A')
ax[1].imshow(dataB, cmap='viridis')
ax[1].set_title('Mask B')
fig.supxlabel('Pixel')
fig.supylabel('Voltage units')
plt.show()

def find_contrast(pixel_data):
    """
    Find contrast of a given pixel data.
    """
    contrast = (max(pixel_data) - min(pixel_data))/max(pixel_data)
    return contrast

def filter_data(mask_data):
    """
    Filter the data using Savitzky-Golay filter.
    """
    filtered_data = []
    for px in range(640):
        data = mask_data[:,px]
        filtered_data.append(savgol_filter(data, window_length=100, polyorder=2))
    return filtered_data

def filter_pixel_range(contrast_threshold=0.75):
    """
    Filter the pixel range based on the contrast threshold.
    """
    filtered_pixel_range = []
    for px in range(640):
        data = dataA[:,px]
        contrast = find_contrast(data)
        if contrast > contrast_threshold:
            filtered_pixel_range.append(px)
    return filtered_pixel_range

def find_trans_peak(data, threshold=0.7, distance=150, width=10):
    """
    Find the peak of the data.
    """
    threshold_height = threshold * max(data)
    peaks, _ = find_peaks(data, height=threshold_height, distance=distance, width=width)
    sorted_peak_indices = np.argsort(data[peaks])[::-1]
    max_values = data[peaks][sorted_peak_indices[:3]]
    return peaks[sorted_peak_indices[:3]]


#filter the data
filtered_data_A = filter_data(dataA)
filtered_data_B = filter_data(dataB)

#find the max(peaks) of Mask A and Mask B
array_A, array_B = [], []
for px in range(640):
    array_A.append(max(find_trans_peak(filtered_data_A[px])))
    array_B.append(max(find_trans_peak(filtered_data_B[px])))

#plot the peaks of Mask A and Mask B
plt.figure()
plt.plot(array_A,label='Mask A')
plt.plot(array_B,label='Mask B')
plt.xlabel('Pixel')
plt.ylabel('Voltage units')
plt.legend()

# Plot the data and filtered data
px_to_plot = 400
print(find_trans_peak(filtered_data_A[px_to_plot]))
plt.figure()
plt.plot(dataA[:,px_to_plot], label='Original Data')
plt.plot(filtered_data_A[px_to_plot], label='Filtered Data')
plt.legend()
plt.xlabel('Voltage units')
plt.ylabel('Intensity')
plt.show()