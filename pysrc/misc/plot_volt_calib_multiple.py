import numpy as np
import matplotlib.pyplot as plt
import os

pixel_range = [200,205]

path = "C:\\Users\\Pubudu Wijesinghe\\Desktop\\SLM_VC_Data"
os.chdir(path)
cnt = 0
data = []

for file in os.listdir():
    if file.endswith(".txt"):
        cnt += 1
        datafile = f"{path}\{file}"
        with open(datafile,'r') as datafile:
            datalist = np.genfromtxt(datafile, delimiter='\t').T
            datalist = datalist[pixel_range[0]:pixel_range[1]]
            data.append(datalist)
    print("file done")

flat_data = [item for sublist in data for item in sublist]

fig = plt.figure()
ax = plt.gca()
plt.imshow(flat_data, interpolation='nearest')
ax.axes.yaxis.set_visible(False)
plt.show()
