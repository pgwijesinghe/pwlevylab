import numpy as np
import os
from tqdm import tqdm

bias_list = np.arange(0, 0.11, 0.02)
for bias in bias_list:
    base_folder = f"G:\\.shortcut-targets-by-id\\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\\ansom\\Data\\THz 1\\SA40663G.20250403\\P-pol_Ins_Bias_New"
    sub_folder = f"Bias{bias}"
    folder_path = os.path.join(base_folder, sub_folder)
    insertion_array = []
    photocurrent_array = []
    num_files = 0

    files = os.listdir(folder_path)
    data_files = [f for f in files if f.endswith('.txt')]

    for file in tqdm(data_files, desc=f'Processing bias {bias}'):
        num_files += 1
        file_path = os.path.join(folder_path, file)
        data = np.loadtxt(file_path, skiprows=1)  # Skip the first row contains headers

        ins = data[:, 0]
        pc = data[:, 1]

        if len(insertion_array) == 0:
            insertion_array = ins
            photocurrent_array = pc
        else:
            photocurrent_array += pc

    photocurrent_array = photocurrent_array / num_files

    combined_array = np.column_stack((insertion_array, photocurrent_array))
  
    output_file =f'averaged_data_{bias}.txt'
    save_file_path = os.path.join(base_folder, output_file)
    np.savetxt(save_file_path, combined_array, delimiter='\t', header='Insertion (mm),Photocurrent (A)')

    