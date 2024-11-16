import matplotlib.pyplot as plt
import numpy as np

# data
z_voltage = np.linspace(-10,10,41)
psj_pos = [0, 2.2, 4.2, 6.2, 8.2, 10.2, 12.2, 14.1, 16.1, 18.0, 20.0, 21.9, 23.8, 25.6, 27.0, 26.7, 26.5, 26.2, 26.0, 25.7, 25.4, 25.1, 24.8, 24.6, 24.3, 24.1, 23.8, 25.2, 27.3, 29.1, 31.0, 32.9, 34.9, 36.9, 38.8, 40.8, 42.9, 44.9, 46.9, 49.0, 51.1]
expected = np.linspace(0,80,41)

fig,ax = plt.subplots()
ax.plot(z_voltage, psj_pos, marker='o', label='actual')
ax.plot(z_voltage, expected, label='expected')
ax.legend()
ax.set_xlabel('Z Voltage (V)')
ax.set_ylabel('Stage Position (um)')
ax.set_title('Graph of Stage position vs. Z Voltage')

plt.show()