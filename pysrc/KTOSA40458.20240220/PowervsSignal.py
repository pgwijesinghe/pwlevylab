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

power = np.array([0.13, 2.36, 4.58, 7.15, 16.51])
signal = np.array([1.65, 3, 4.4, 5.5, 13.8])

plt.plot(power, signal, 'ro-')
plt.xlabel('Power (mW)')
plt.ylabel('4T Conductance (uS)')
plt.show()
