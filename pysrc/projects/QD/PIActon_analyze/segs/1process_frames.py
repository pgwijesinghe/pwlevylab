'''
File structure: 
100 (stripes) x 1340 (pixels) lines
Each line has 3 values separated by commas: wavelength, stripe, intensity

This will sum the intensities for each wavelength across all stripes and save the results to a new file.
'''

import os
import glob

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

def main(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each input file
    input_files = glob.glob(os.path.join(input_folder, '*.txt'))
    for input_file in input_files:
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_folder, file_name)
        process_file(input_file, output_file)
        print(f"Processed {input_file} -> {output_file}")

# Define the input and output folders
input_folder = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Qdots spectra\exp2"
output_folder = r"C:\Users\Pubudu Wijesinghe\Desktop\output"

# Run the main function
main(input_folder, output_folder)