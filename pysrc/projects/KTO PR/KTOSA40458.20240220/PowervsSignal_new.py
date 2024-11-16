"""
Setup:
4T Measurement of Conductance (Lockin-time) vs. Different Power levels (Power was measured going into the enclosure)
20mV AC 13Hz Lockin Signal
Data file: "G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40458.20240220\00 - Monitor Contrast\SA40458.20240220.000007.tdms"
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')

power = np.array([0.08, 0.23, 1.29, 2.75, 3.85, 4.16])
signal = np.array([2.8, 3.4, 3.95, 4.6, 5.2, 5.58])
sig = np.array([2.75, 3.03, 3.45, 3.6, 3.88, 3.98])

sig2 = np.array([0.6, 1.05, 1.7, 2.2, 2.53, 2.53])
plt.plot(power, signal, 'go-')
# plt.plot(power, sig2, 'ro-')
plt.xlabel('Power (mW)')
plt.ylabel('4T Conductance (uS)')
plt.show()
