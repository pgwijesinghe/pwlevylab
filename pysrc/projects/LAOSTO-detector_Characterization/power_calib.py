import matplotlib.pyplot as plt
import numpy as np

# Element 2
apd_e2 = np.array([1.2, 5.6, 7.2, 9, 10])
power_e2 = np.array([8.7, 27.4, 34, 41.6, 44.5])

#HeNe
apd_hene = np.array([5.8, 8, 9.8, 12.8, 16])
power_hene = np.array([4.3, 6.2, 7.8, 9.8, 12])

# linear fit using scipy
from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(apd_hene, power_hene)
print(slope, intercept, r_value, p_value, std_err)

plt.plot(apd_e2, power_e2, label='Element 2')
plt.plot(apd_hene, power_hene, label='HeNe')
plt.show()