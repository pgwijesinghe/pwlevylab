# Crystal Test with Transmission mode just after the laser
# Optical flow: Laser -> Filter Config -> 10X Objective -> BBO -> Blue Filter -> Spectrometer

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

power_BBO = np.array([0.6, 20.2, 21.5, 54.4, 56.2, 145, 154.5, 475])
power_SHG = np.array([0.43, 0.62, 0.68, 2.3, 2.9, 11.2, 15.6, 117])

################# FITTING ###################################
# objective function
def objective(x, a):
	return a * x**2
# fit curve
popt, _ = curve_fit(objective, power_BBO, power_SHG)
# define new input values
x_new = np.arange(0, max(power_BBO), 0.1)
# unpack optima parameters for the objective function
a = popt
# use optimal parameters to calculate new values
y_new = objective(x_new, a)
#############################################################

plt.plot(power_BBO,power_SHG,'x',color='red',label='data')
plt.plot(x_new,y_new,color='black',label='fit')
plt.title("SHG Power vs. BBO Power (Transmission Mode)")
plt.xlabel("Power @ BBO (mW)")
plt.ylabel("Power @ SHG (uW)")
plt.legend()
plt.show()
print(a)
