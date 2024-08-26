'''
This will read the averaged intensities from the final output file and plots them.
'''

import matplotlib.pyplot as plt

def plot_averaged_intensities(input_file):
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
    plt.plot(wavelengths, intensities, label='Averaged Intensity')
    plt.xlabel('Wavelength')
    plt.ylabel('Averaged Intensity')
    plt.title('Averaged Intensity vs. Wavelength')
    plt.legend()
    plt.grid(True)
    plt.show()

# Define the input file
input_file = r"C:\Users\Pubudu Wijesinghe\Desktop\final.txt"

# Run the plotting function
plot_averaged_intensities(input_file)
