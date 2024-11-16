import matplotlib.pyplot as plt

# data
x = [-10, 0, 10, 20, 70, 88, 150]
y1 = [100,90,75,65,0,-20,-100]
y2 = [79.1,69.2,59.4,49.5,0,-17.7,-19.6]

fig,ax = plt.subplots()

ax.plot(x, y1, marker='o', color='green')
ax.vlines(88, -100, 100, color='red', ls='dashed', label='PSJC OOR limit')
ax.set_xlabel('Igor S/W Voltage (V)')
ax.set_ylabel('OSC Reading (V)', color='green')
ax.legend()

ax2=ax.twinx()
ax2.plot(x, y2, marker='o', color='blue')
ax2.set_ylabel('PSJC Reading (um)', color='blue')


plt.show()