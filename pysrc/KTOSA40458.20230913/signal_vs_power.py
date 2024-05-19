import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.style.use('ggplot')

power_array = np.array([0.01e-6, 0.3e-6, 0.8e-6, 1.3e-6, 1.6e-6])
signal_array = np.array([0.56e-6, 1.2e-6, 1.6e-6, 1.9e-6, 2.2e-6])

# Fit a linear regression line
coefficients = np.polyfit(power_array, signal_array, 1)
line = np.poly1d(coefficients)

# Plot the data and the linear regression line
plt.figure()
plt.plot(power_array, signal_array, '-o', color='green')
# plt.plot(power_array, line(power_array), '--', color='blue')
plt.xlabel("Power (W)")
plt.ylabel("4T Conductance (S)")
plt.show()