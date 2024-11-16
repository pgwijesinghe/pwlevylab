import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_dict = {}

# Load the data
with open('data.dat', 'r') as f:
    data = f.readlines()
    for i in range(len(data)):
        if data[i].startswith('\tTrajectory'):
            trajectory = data[i].split()[1]
            
            data_dict.update({trajectory: 'a'})


