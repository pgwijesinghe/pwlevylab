import numpy as np
import matplotlib.pyplot as plt

_in_to_mm = 25.4

# Distance from the Laser aperture to the 5 mirrors
distance = np.array([17, 63, 74, 87, 103])*_in_to_mm
# r_x = np.array([0.902, 1.287, 1.468, 1.941, 2.255])/2 
# r_y = np.array([0.905, 1.545, 1.771, 1.716, 1.969])/2 

# Beam diameters for the x and y directions (in mm) from Beam profiler
r_x = np.array([0.94, 1.55, 1.74, 1.95, 2.22])/2 
r_y = np.array([0.90, 1.30, 1.49, 1.70, 2.05])/2

def process_data(x):
    coefficients = np.polyfit(distance, x, 1)
    fit = np.polyval(coefficients, distance)
    gradient = coefficients[0]
    intercept = coefficients[1]
    root = np.roots(coefficients)
    return coefficients, fit, gradient, intercept, root

coefficients_x, fit_x, gradient_x, intercept_x, root_x = process_data(r_x)
coefficients_y, fit_y, gradient_y, intercept_y, root_y = process_data(r_y)

# Print Data
gradients = (gradient_x, gradient_y)
intercepts = (intercept_x, intercept_y)
roots = (root_x, root_y)
print("Gradient of (x, y):", gradients)
print("Intercept of (x, y):", intercepts)
print("roots (x, y):", roots)

# Plotting Data
fig, ax = plt.subplots(1,2, figsize=(10,5))
ax[0].plot(distance, r_x, 'o', label='Data')
ax[0].plot(distance, fit_x, label='Linear Fit')
ax[0].set_xlabel('Distance')
ax[0].set_ylabel('d_x')
ax[0].legend()
ax[1].plot(distance, r_y, 'o', label='Data')
ax[1].plot(distance, fit_y, label='Linear Fit')
ax[1].set_xlabel('Distance')
ax[1].set_ylabel('d_y')
ax[1].legend()
plt.show()


