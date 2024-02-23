import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.style.use('ggplot')

power_array = np.array([5e-3, 15e-3, 35e-3, 40e-3, 50e-3])
signal_array = np.array([3.5e-6, 4.5e-6, 6.5e-6, 7.2e-6, 8e-6])

plt.figure()
plt.plot(power_array, signal_array, '-o', color='red')
plt.xlabel("Bias (V)")
plt.ylabel("4T Conductance (S)")
plt.show()