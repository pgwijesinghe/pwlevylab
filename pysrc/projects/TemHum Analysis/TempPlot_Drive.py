import pandas as pd
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\Pubudu's Data\THz1_TempHum Analysis\GDrive Data\New folder\\"
datetime = np.array([])
temp = np.array([])
xticks = np.array([])

for datafile in os.listdir(path):
    df = pd.read_csv(path +  datafile)
    df = df[df.index % 5 == 0]
    temps = df['202 temp'].values.astype(np.float64)
    temps = (temps-32)*(5/9)
    temp = np.append(temp, temps)
    datetime = np.append(datetime, df['Date Range'].values)
    print(datafile)
    
xticks = np.append(xticks, datetime[::500])

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 15}

matplotlib.rc('font', **font)


plt.plot(datetime, temp)
plt.title("TempHum Data @ NPL202 (6/30 - 9/28) (from GDrive)")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (C)")
plt.xticks(xticks)
plt.ylim(18,23)
plt.show()