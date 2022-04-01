from stat import ST_SIZE
import numpy as np
import matplotlib.pyplot as plt
import os

sp_lim = [380, 1080]  # in nm
plt_xrange = [300,1200]  # in nm 

path = r"G:\My Drive\ansom\users\Pubudu\Reflection Spectrum"
os.chdir(path)

fig = plt.figure()
plt.xlabel("Wavelength (nm)")
plt.ylabel("Strength")
plt.title("Spectrum")
for file in os.listdir():
    if file.endswith(".txt") and os.stat(file).st_size != 0:
        datafile = f"{path}\{file}"
        with open(datafile,'r') as datafile:
            datalist = np.genfromtxt(datafile, delimiter='\t')
            x_scale = [sp_lim[0] + (sp_lim[1]-sp_lim[0])*i/len(datalist) for i in range(len(datalist))]
            plt.plot(x_scale, datalist, label=file)
plt.yscale('log')
plt.xlim(plt_xrange[0], plt_xrange[1])
plt.legend()
plt.show()