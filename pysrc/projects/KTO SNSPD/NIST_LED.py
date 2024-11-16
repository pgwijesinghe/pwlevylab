import matplotlib.pyplot as plt

x = [2,70,300]
Vf_1650 = [0.94, 1.15, 0.49]
Vf_935 = [1.33,1.59,1.02]
Vf_650 = [7.45,9.1,1.66]

plt.plot(x, Vf_1650, x, Vf_935, x, Vf_650)
plt.show()