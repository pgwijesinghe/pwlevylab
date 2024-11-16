"""
Pinhole experiment to find the optimal focus for SHG and reference wavelengths
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = 750 # reference wavelength
y = 400 # SHG wavelength

px = np.array([280,350,380,450]) # pixel array
x_values = np.array([784,747,730,689]) # corresponding wavelengths
y_values = np.array([41.5,42,42.5,43.5]) # Zmax array

# objective function
def objective(x, a, b, c):
	return a * x + b * x**2 + c

# fit curve
popt, _ = curve_fit(objective, x_values, y_values)

# define new input values
x_new = np.arange(350, max(x_values), 1)
# unpack optima parameters for the objective function
a, b, c = popt
# use optimal parameters to calculate new values
y_new = objective(x_new, a, b, c)
ref_z = y_new[list(x_new).index(x)]
shg_z = y_new[list(x_new).index(y)]
str = f"Relative movement from {x} nm to {y} nm is: {round(shg_z - ref_z,2)} um"
print(str)

plt.plot(x_values,y_values,'x',color='red',label='data')
plt.plot(x_new,y_new,color='black',label='fit')
plt.vlines([x],min(y_new),max(y_new),linestyle='dashed',label='REF WL',color='red')
plt.vlines([y],min(y_new),max(y_new),linestyle='dashed',label='SHG WL',color='blue')
plt.xlabel(f'Wavelength (nm)\n\n{str}')
plt.ylabel('Z height (um)')
plt.title('Zmax vs. Wavelength (100X/Element2)')
plt.legend()
plt.show()