import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

path = "C:\\Users\\pubud\\Desktop\\Data\\"
datetime = np.array([])
temp = np.array([])
xticks = np.array([])

for datafile in os.listdir(path):
    df = pd.read_csv(path +  datafile, names=["idx", "temp", "hum1", "hum2", "datetime"])
    df = df[df.index % 1000 == 0]
    temp = np.append(temp, df.iloc[:,1].values)
    datetime = np.append(datetime, df.iloc[:,4].values)
    xticks = np.append(xticks, df.iloc[:,4].values[0])

print(f"Temp Min:{min(temp)} Temp Max:{max(temp)}")

plt.plot(datetime, temp)
plt.title("TempHum Data @ THz1 (9/11 - 9/28)")
plt.xlabel("Date/Time")
plt.ylabel("Temperature(C)")
plt.xticks(xticks)
plt.ylim(25,30)
plt.show()