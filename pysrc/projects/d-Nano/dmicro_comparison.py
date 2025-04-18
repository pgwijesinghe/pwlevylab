import numpy as np
import matplotlib.pyplot as plt

# Function to load and process the data from the file
def load_spectrum_data(file_path):
    # Open the file
    with open(file_path, 'r') as file:
        # Read the first line to get nWL (number of wavelength points)
        line1 = file.readline().strip()
        nWL = int(line1.split('=')[1])

        # Read the second line to get nI (number of insertion points)
        line2 = file.readline().strip()
        nI = int(line2.split('=')[1])

        # Read the next nWL lines for the wavelength array
        wavelength = np.array([float(file.readline().strip()) for _ in range(nWL)])

        # Read the next nI lines for the insertion array
        insertion = np.array([float(file.readline().strip()) for _ in range(nI)])

        # Initialize an empty array for the spectrum data
        spectrum_data = np.zeros((nI, nWL))

        # Read the spectrum data for each insertion point
        for i in range(nI):
            # Read the next 2048 (nWL) lines for the spectrum at this insertion point
            spectrum = np.array([float(file.readline().strip()) for _ in range(nWL)])
            # Store this spectrum in the correct position in the array
            spectrum_data[i] = spectrum

        # Return the data
        return wavelength, insertion, spectrum_data

# Function to plot the heatmap
def plot_heatmap(wavelength, insertion, spectrum_data):
    plt.figure(figsize=(10, 6))
    plt.imshow(spectrum_data, aspect='auto', cmap='jet', origin='lower', extent=[wavelength[0], wavelength[-1], insertion[0], insertion[-1]])
    plt.colorbar(label='Intensity')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Insertion (mm)')
    plt.title('Intensity vs Wavelength vs Insertion (Heatmap)')
    plt.show()

# Function to extract and plot a linecut for a given wavelength
def plot_linecut_at_wavelength(wavelength, insertion, spectrum_data, target_wavelength):
    # Find the index of the closest wavelength to the target wavelength
    wavelength_index = np.abs(wavelength - target_wavelength).argmin()

    # Get the closest wavelength
    closest_wavelength = wavelength[wavelength_index]

    # Extract the intensity values at this wavelength for all insertion points
    intensity_at_wavelength = spectrum_data[:, wavelength_index]

    # Print the closest wavelength found
    print(f"Closest wavelength to {target_wavelength} nm is {closest_wavelength} nm")

    # Plot the linecut (Intensity vs Insertion)
    plt.figure(figsize=(10, 6))
    plt.plot(insertion, intensity_at_wavelength, label=f'Linecut at {closest_wavelength} nm')
    plt.xlabel('Insertion (mm)')
    plt.ylabel('Intensity')
    plt.title(f'Linecut of Intensity vs Insertion at {closest_wavelength} nm')
    plt.legend()
    plt.grid(True)
    plt.show()
    # Save the linecut data to a text file
    output_data = np.column_stack((insertion, intensity_at_wavelength))
    output_filename = f'linecut_data_{closest_wavelength:.1f}nm.txt'
    np.savetxt(output_filename, output_data, header=f'Insertion (mm)\tIntensity at {closest_wavelength:.1f} nm', delimiter='\t')

# Example usage
file_path = r"C:\Users\PubuduW\Desktop\ret_20250307_153008_measured_dmicro.txt"  # Replace with the path to your text file
wavelength, insertion, spectrum_data = load_spectrum_data(file_path)

# Plot the heatmap
plot_heatmap(wavelength, insertion, spectrum_data)

# Extract and plot a linecut at a specified wavelength
target_wavelength = 380  # Replace with the desired wavelength (in nm)
plot_linecut_at_wavelength(wavelength, insertion, spectrum_data, target_wavelength)
