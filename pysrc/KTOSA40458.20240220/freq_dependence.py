"""
Lockin Params: 30ms, 50mv, 12dB
Used the reflective chopper with Agilent 8820A to control the frequency
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.style.use('ggplot')

freq = np.array([500,600,700,800,900,1000,1100,1200,1300,1400,1600,1700,1800,1900,2000,2200,2300,2400, 2500, 2600, 2700, 2800, 2900, 3000])
sig = np.array([-18, -17, -15, -10, -8, -6, -5, -3.5, -3, -2.3, -1.5, -1.3, -1.1, -1.1, -0.9, -0.8, -0.7, -0.65, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6])

plt.plot(freq, -sig)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Signal (arb)')
plt.show()