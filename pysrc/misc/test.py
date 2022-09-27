# import numpy as np
# import matplotlib.pyplot as plt
# import os
# from scipy.signal import find_peaks
# from scipy.signal import savgol_filter

# pixel_range = [150,400]

# path = "C:\\Users\\Pubudu Wijesinghe\\Desktop\\"
# os.chdir(path)
# cnt = 0
# data = []
# file = 'Mask A.txt'
# datafile = f"{path}\{file}"
# with open(datafile,'r') as datafile:
#     data = np.genfromtxt(datafile, delimiter='\t')
#     data = data.T

# arr = data[300]
# arr = savgol_filter(arr, 51, 2)
# peaks, _ = find_peaks(arr, height=12000, distance=200) # also check the distance parameter

# plt.plot(arr)
# plt.plot(peaks,arr[peaks], "x")
# plt.show()


# Crystal Test with Transmission mode just after the laser
# Optical flow: Laser -> Filter Config -> 10X Objective -> BBO -> Blue Filter -> Spectrometer

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

power_BBO = np.array([21.5, 54.4, 56.2, 145, 154.5, 475])
power_SHG_Spectr = np.array([290, 560, 900, 2400, 5250, 53000])

################# FITTING ###################################
# objective function
def objective(x, a):
	return a * x**2
# fit curve
popt, _ = curve_fit(objective, power_BBO, power_SHG_Spectr)
# define new input values
x_new = np.arange(0, max(power_BBO), 0.1)
# unpack optima parameters for the objective function
a = popt
# use optimal parameters to calculate new values
y_new = objective(x_new, a)
#############################################################

plt.plot(power_BBO,power_SHG_Spectr,'x',color='red',label='data')
plt.plot(x_new,y_new,color='black',label='fit')
plt.title("SHG Power vs. BBO Power (Transmission Mode)")
plt.xlabel("Power @ BBO (mW)")
plt.ylabel("Power @ SHG @ Spectrometer")
plt.legend()
plt.show()
print(a)

