import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks
from scipy.signal import savgol_filter

pixel_range = [150,400]

path = "C:\\Users\\Pubudu Wijesinghe\\Desktop\\"
os.chdir(path)
cnt = 0
data = []
file = 'Mask A.txt'
datafile = f"{path}\{file}"
with open(datafile,'r') as datafile:
    data = np.genfromtxt(datafile, delimiter='\t')
    data = data.T

arr = data[300]
arr = savgol_filter(arr, 51, 2)
peaks, _ = find_peaks(arr, height=12000, distance=200) # also check the distance parameter

plt.plot(arr)
plt.plot(peaks,arr[peaks], "x")
plt.show()

