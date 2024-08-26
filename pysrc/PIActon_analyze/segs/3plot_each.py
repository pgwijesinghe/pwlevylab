'''
This will read a summed intensity file and plot it vs. wavelength.
'''

import matplotlib.pyplot as plt

def plot_intensities(input_file):
    wavelengths = []
    intensities = []

    # Read the averaged intensities file
    with open(input_file, 'r') as f:
        for line in f:
            wavelength, intensity = line.strip().split(',')
            wavelengths.append(float(wavelength))
            intensities.append(float(intensity))

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, intensities, label='Summed Intensity')
    plt.xlabel('Wavelength')
    plt.ylabel('Summed Intensity')
    plt.title('Summed Intensity vs. Wavelength for ' + input_file)
    plt.legend()
    plt.grid(True)
    plt.show()

# Define the input file
input_file = r"C:\Users\Pubudu Wijesinghe\Desktop\output\test29_1160.txt"

# Run the plotting function
plot_intensities(input_file)
