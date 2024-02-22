from nptdms import TdmsFile

I_plus = "Time"
I_minus = "AO1"
V_plus = "AI1"
V_minus = "AI2"
Vsource = 100e-3

tdms_file_path = "./datafile.tdms"
with TdmsFile.open(tdms_file_path) as tdms_file:
    I_plus_data = tdms_file[tdms_file.groups()[0].name][I_plus][:]
    I_minus_data = tdms_file[tdms_file.groups()[0].name][I_minus][:]
    V_plus_data = tdms_file[tdms_file.groups()[0].name][V_plus][:]
    V_minus_data = tdms_file[tdms_file.groups()[0].name][V_minus][:]

print(I_plus_data)
print(I_minus_data)


