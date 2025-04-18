import os
import numpy as np

folder_path = f"G:\\.shortcut-targets-by-id\\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\\ansom\\Data\\THz 1\\SA40663G.20250403\\P-pol_Ins_Bias_New\\avg_data"

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))

files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

normalize_data = False

for file in files:
    data = np.loadtxt(os.path.join(folder_path, file))
    x_data, y_data = data[:, 0], data[:, 1]
    y_normalized = (y_data - np.min(y_data)) / (np.max(y_data) - np.min(y_data))
    plt.plot(data[:, 0], y_normalized, label=file) if normalize_data else plt.plot(data[:, 0], y_data, label=file)


plt.xlabel('X')
plt.ylabel('Y') 
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()