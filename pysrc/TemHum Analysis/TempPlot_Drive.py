import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

path = "C:\\Users\\pubud\\Desktop\\THz1_TempHumData\\GDrive\\"
datetime = np.array([])
temp = np.array([])
xticks = np.array([])

for datafile in os.listdir(path):
    df = pd.read_csv(path +  datafile)
    df = df[df.index % 5 == 0]
    temp = np.append(temp, df['202 temp'].values)
    datetime = np.append(datetime, df['Date Range'].values)
    
xticks = np.append(xticks, datetime[::100])

plt.plot(datetime, temp)
plt.title("TempHum Data @ NPL202 (9/11 - 9/28) (from GDrive)")
plt.xlabel("Date/Time")
plt.ylabel("Temperature (F)")
plt.xticks(xticks)
plt.ylim(65,70)
plt.show()