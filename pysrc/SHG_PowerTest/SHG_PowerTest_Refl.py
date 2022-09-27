# SHG Test with Reflection mode just after the laser
# Optical flow: Laser -> (HWP -> Pol) -> DCBS -> Obj1 <-> BBO
#                                     APD <-

# Obj1 = OFR LLO-4-18 (10X)
# Input Polarization = Vertical (90)
# BBO Angle = 67
# Holder Angle = 120 

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

APD_Gain = 2.5e6

noisy_x = np.array([0.32, 2, 3])
noisy_y = np.array([0.2, 0.2, 0.2])*1e-6
power_BBO = np.array([5.1, 10, 16, 54, 64.6, 80, 85.5, 115, 131])
APD_signal = np.array([1.3, 6.3, 14, 178, 257, 390, 420, 874, 1070])*1e-6
power_APD = APD_signal*1e9/APD_Gain
noise_level = 0.2e-6/APD_Gain
################# FITTING ###################################
# objective function
def objective(x, a):
	return a * x**2
# fit curve
popt, _ = curve_fit(objective, power_BBO, power_APD)
# define new input values
x_new = np.arange(0, max(power_BBO), 0.1)
# unpack optima parameters for the objective function
a = popt
# use optimal parameters to calculate new values
y_new = objective(x_new, a)
#############################################################

plt.plot(power_BBO,power_APD,'x',color='red',label='data')
plt.plot(x_new,y_new,color='black',label='fit')
plt.plot(noisy_x,noisy_y,'x',color='orange',label='data')
plt.hlines([noise_level],min(x_new),max(x_new),linestyle='dashed',label='Noise Level',color='blue')
plt.title("SHG Power vs. BBO Power (Reflection Mode)")
plt.xlabel("Power @ BBO (mW)")
plt.ylabel("Power @ APD (nW)")
plt.legend()
plt.show()
print(a)