"""
Upon replacing the DUT with a mirror and observing the reflection signal with the SPD, it gave a significant signal.
This is observing the SPD signal vs. Input power of the Mira900 (Measured at the static iris) to check whether there's a non=linearity
If it's a nonlinear signal, the mirror is damaged.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.style.use('ggplot')

power_array = np.array([40, 37, 31, 23.5, 16.2, 14.3, 9.14, 8.6])
signal_array = np.array([2000, 1500, 900, 400, 280, 140, 60, 35])

plt.figure()
plt.plot(power_array, signal_array, '-o', color='red')
plt.xlabel("Input Power (mW) (at Aperture 1)")
plt.ylabel("SPD Int Counts")
plt.show()