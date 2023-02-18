import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

path = "C:\\Users\\Pubudu Wijesinghe\\Desktop\\New folder (2)\\June\\"
datetime = np.array([])
temp = np.array([])
xticks = np.array([])

for datafile in os.listdir(path):
    df = pd.read_csv(path +  datafile)
    df = df[df.index % 5 == 0]
    temp = np.append(temp, df['202 temp'].values)
    datetime = np.append(datetime, df['Date Range'].values)
    
df_new = pd.DataFrame({'x':datetime, 'y':temp})
df_new.to_csv('test.csv')