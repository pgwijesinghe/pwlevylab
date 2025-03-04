import numpy as np
import matplotlib.pyplot as plt

# Paths to the two processed data files
processed_data_file_1 = r"./data/processed.npz"
processed_data_file_2 = r"./data_ref/processed.npz"

# Load the data from both files
data_1 = np.load(processed_data_file_1)
data_2 = np.load(processed_data_file_2)

# Extract frequencies, B fields, and log magnitude S21
frequencies_1 = data_1["frequencies"]
b_fields_1 = data_1["b_fields"]
log_magnitude_s21_1 = data_1["log_magnitude_s21"]

frequencies_2 = data_2["frequencies"]
b_fields_2 = data_2["b_fields"]
log_magnitude_s21_2 = data_2["log_magnitude_s21"]

# Ensure the frequencies and b_fields are the same in both datasets
if not np.array_equal(frequencies_1, frequencies_2):
    raise ValueError("Frequencies in the two files do not match.")
if not np.array_equal(b_fields_1, b_fields_2):
    raise ValueError("B fields in the two files do not match.")

# Subtract the data (log magnitude of S21) from the two files
log_magnitude_diff = log_magnitude_s21_1 - log_magnitude_s21_2

# Plot the difference as a heatmap
fig, ax = plt.subplots(figsize=(12, 8))
c = ax.pcolormesh(b_fields_1, frequencies_1, log_magnitude_diff.T, cmap="copper", shading="auto")
ax.set_xlabel("B field")
ax.set_ylabel("Frequency (Hz)")
ax.set_title("Difference in Log Magnitude of S21 (dB) Heatmap")
fig.colorbar(c, ax=ax, label="Difference in |S21| (dB)")

plt.show()
