'''
This will compute the average intensity for each wavelength across all input files and save the results to a new file.
'''

import os
import glob

def compute_average(input_folder, output_file):
    # Dictionary to store the sum of intensities for each wavelength
    intensity_sums = {}
    num_files = 0

    # List all input files
    input_files = glob.glob(os.path.join(input_folder, '*.txt'))

    for input_file in input_files:
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

def main(input_folder, output_file):
    compute_average(input_folder, output_file)
    print(f"Averages computed and saved to {output_file}")

# Define the input folder and output file
input_folder = r"C:\Users\Pubudu Wijesinghe\Desktop\output"
output_file = r"C:\Users\Pubudu Wijesinghe\Desktop\final.txt"

# Run the main function
main(input_folder, output_file)
