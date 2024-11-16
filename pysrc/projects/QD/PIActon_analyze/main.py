'''
File structure: 
100 (stripes) x 1340 (pixels) lines
Each line has 3 values separated by commas: wavelength, stripe, intensity

This script will: 
1. Sum the intensities for each wavelength across all stripes for each frame in input_folder and save the results to files in output_folder.
2. Average the intensities across all frames and save the results to aa_final.txt.
3. Plot the averaged intensities.
'''

import os
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

# Define the input and output folders
input_folder = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Qdots spectra\exp2"
output_folder = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Qdots spectra\processed"
output_file = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Qdots spectra\processed\aa_final.txt"

def process_file(input_file, output_file):
    # Dictionary to store the sum of intensities for each wavelength
    intensity_sums = {}

    # Open the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            wavelength, stripe, intensity = line.strip().split(',')
            wavelength = float(wavelength)
            intensity = float(intensity)

            if wavelength not in intensity_sums:
                intensity_sums[wavelength] = 0
            intensity_sums[wavelength] += intensity

    # Write the results to the output file
    with open(output_file, 'w') as f:
        for wavelength in sorted(intensity_sums.keys()):
            f.write(f"{wavelength},{intensity_sums[wavelength]}\n")

def process(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each input file
    input_files = glob.glob(os.path.join(input_folder, '*.txt'))
    for input_file in tqdm(input_files, desc="Processing files"):
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, file_name)
        process_file(input_file, output_file)

def compute_average(input_folder, output_file):
    # Dictionary to store the sum of intensities for each wavelength
    intensity_sums = {}
    num_files = 0

    # List all input files
    input_files = glob.glob(os.path.join(input_folder, '*.txt'))

    for input_file in tqdm(input_files, desc="Computing averages"):
        num_files += 1
        with open(input_file, 'r') as f:
            for line in f:
                wavelength, intensity = line.strip().split(',')
                wavelength = float(wavelength)
                intensity = float(intensity)

                if wavelength not in intensity_sums:
                    intensity_sums[wavelength] = 0
                intensity_sums[wavelength] += intensity

    # Compute the average intensities
    average_intensities = {wavelength: intensity / num_files for wavelength, intensity in intensity_sums.items()}

    # Write the averages to the output file
    with open(output_file, 'w') as f:
        for wavelength in sorted(average_intensities.keys()):
            f.write(f"{wavelength},{average_intensities[wavelength]}\n")

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

# Run the main function
process(input_folder, output_folder)
print(f"Processed all files in {input_folder} and saved to {output_folder}")
print(f"Computing averages and saving to {output_file}...")
compute_average(output_folder, output_file)
print(f"Averages computed and saved to {output_file}")
print("Plotting the averaged intensities...")
plot_averaged_intensities(output_file)
