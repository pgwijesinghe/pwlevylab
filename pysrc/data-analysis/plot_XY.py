from nptdms import TdmsFile
import matplotlib.pyplot as plt

tdms_folder_path = ""
tdms_file_path = r"C:\Users\Pubudu Wijesinghe\Desktop\SA40458.20230904.000009.tdms"

# # define leads
# I_plus, I_minus = 1,3
# V_plus, V_minus = 2,4
# V_bg = 6

# plot type could be IV or XY
def plot_2D(plot_type='IV', x='Time', y='G', Ipm=(1,3), Vpm=(2,4), source=100e-3):
    if plot_type == 'IV':
        with TdmsFile.open(tdms_file_path) as tdms_file:
            V_2T =  tdms_file[tdms_file.groups()[0].name][f'AO{Ipm[0]}'][:]
            I_m = tdms_file[tdms_file.groups()[0].name][f'AI{Ipm[1]}'][:]
            V_p = tdms_file[tdms_file.groups()[0].name][f'AI{Vpm[0]}'][:]
            V_m = tdms_file[tdms_file.groups()[0].name][f'AI{Vpm[1]}'][:]
            V_4T = V_p - V_m
            plt.plot(V_2T,I_m)
            # plt.plot(V_4T,I_m)
            plt.show()
    elif plot_type == 'XG' or plot_type=='XR':
        with TdmsFile.open(tdms_file_path) as tdms_file:
            X = tdms_file[tdms_file.groups()[0].name][x][:]
            I_p = tdms_file[tdms_file.groups()[0].name][f'X{Ipm[0]}'][:]
            I_m = tdms_file[tdms_file.groups()[0].name][f'X{Ipm[1]}'][:]
            V_p = tdms_file[tdms_file.groups()[0].name][f'X{Vpm[0]}'][:]
            V_m = tdms_file[tdms_file.groups()[0].name][f'X{Vpm[1]}'][:]
            V_4T = V_p - V_m
            G_2T = I_m/source
            G_4T = I_m/V_4T
            plt.plot(X,G_2T) if plot_type=='XG' else plt.plot(X,1/G_4T)
            plt.show()
    return None

plot_2D(plot_type='IV', x='Time', source=10e-3)
