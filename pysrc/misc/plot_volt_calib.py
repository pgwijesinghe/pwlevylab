import numpy as np
import matplotlib.pyplot as plt
import os

path = "C:\\Users\\Pubudu Wijesinghe\\Desktop\\SLM_VC_Data"
os.chdir(path)
cnt = 0

for file in os.listdir():
    if file.endswith(".txt"):
        cnt += 1
        datafile = f"{path}\{file}"
        with open(datafile,'r') as datafile:
            data = np.genfromtxt(datafile, delimiter='\t')
        imgname = file.split(".")[0]
        plt.figure()
        plt.title(file)
        # plt.imshow(np.transpose(data))
        plt.plot(data)
        plt.savefig(f"data{imgname}")
        print(f"{cnt} files done")
        # plt.show()

