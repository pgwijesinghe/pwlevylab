import numpy as np

power = np.array([30, 25, 20, 15, 10, 35, 40])*0.3
shg_counts = np.array([50, 38, 28, 15, 8, 70, 90])

# Fit the data to a quadratic function
coefficients = np.polyfit(power, shg_counts, 2)
quadratic_fit = np.poly1d(coefficients)

# Print the coefficients
print("Quadratic coefficients:", coefficients)

# Generate points for plotting the fit
power_fit = np.linspace(min(power), max(power), 100)
shg_fit = quadratic_fit(power_fit)

# Plot the data and the fit
import matplotlib.pyplot as plt

plt.scatter(power, shg_counts, label='Data')
plt.plot(power_fit, shg_fit, label='Quadratic fit', color='red')
plt.xlabel('Power (mW)')
plt.ylabel('SHG Counts')
plt.legend()
plt.show()
