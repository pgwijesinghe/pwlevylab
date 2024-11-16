import numpy as np
import matplotlib.pyplot as plt

datafile = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\20240205\SLM single px cal\Mask A\Mask A_600"
data = np.genfromtxt(datafile, delimiter='\t')

voltages = data[:,0]
spectrum = data[:,3648:]
spectrum = np.transpose(spectrum)
plt.imshow(spectrum, cmap='viridis', extent=[min(voltages), max(voltages), 0, 3648])
plt.show()