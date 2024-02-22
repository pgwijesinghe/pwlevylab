from nptdms import TdmsFile
import matplotlib.pyplot as plt

Vsource = "AO1"
I_plus = "AI1"
I_minus = "AI3"
V_plus = "AI2"
V_minus = "AI4"

tdms_file_path = "./datafile.tdms"
with TdmsFile.open(tdms_file_path) as tdms_file:
    Vsource_data =  tdms_file[tdms_file.groups()[0].name][Vsource][:]
    I_plus_data = tdms_file[tdms_file.groups()[0].name][I_plus][:]
    I_minus_data = tdms_file[tdms_file.groups()[0].name][I_minus][:]
    V_plus_data = tdms_file[tdms_file.groups()[0].name][V_plus][:]
    V_minus_data = tdms_file[tdms_file.groups()[0].name][V_minus][:]
    V_2T = Vsource_data
    V_4T = V_plus_data - V_minus_data

plt.figure()
plt.plot(V_2T,I_minus_data)
plt.show()


