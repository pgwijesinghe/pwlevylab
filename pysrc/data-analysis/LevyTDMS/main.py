from LevyTDMS import LevyTDMS
import numpy as np
import matplotlib.pyplot as plt

# files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40663G.20250429\20250430_HighRes_2")
# files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\03 - 20250526_CtrlExp")
# files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\10 - 20250604_CtrlExp") 
# files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\14 - 20250604_CtrlExp_UnequalDispersion")
files = LevyTDMS(r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\20 - 20250617_CtrlExp_Run3_50mBias") 


data = files.extract_channels(
    channels={'Data.000000': ['Delay', 'Ch3_PS_y', 'Ch3_PS_x', 'Ch3_y', 'Insertion']},
    # cache_file="extracted_data__no_nanorod.npz"
    # cache_file="test.npz"
)
x = np.concatenate([d['Insertion'] for d in data])
y = np.array([np.max(d['Ch3_y']) for d in data])
plt.plot(x,y)
plt.show()

filtered_data = files.apply_frequency_filter(
    data,
    signal_key='Ch3_y',
    delay_key='Delay',
    bands_THz=[(0, 30), 
               (350, 450), 
               (700, 900),
               ]
)

files.plot_heatmap_1(
    extracted_data=filtered_data,
    sig_channel='Ch3_y_filtered',
    x_channel='Delay',
    y_channel='Insertion',
    title='TD vs GDD (Filtered)',
    xlabel='Delay [ps]',
    ylabel='Insertion [mm]'
)

files.plot_PS(
    extracted_data=data,
    sig_channel='Ch3_PS_y',
    x_channel='Ch3_PS_x',
    y_channel='Insertion',
    title='Power Spectrum (log) vs GDD',
    xlabel='Frequency [THz]',
    ylabel='Insertion [mm]'
)