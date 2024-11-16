import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.style.use('ggplot')

fig, ax = plt.subplots()
ax.set_xlim(-80, 80)
ax.set_ylim(0, 100)
for frame in range(2000):
    datafile = f'trajs\\block_{frame}.txt'
    x, y, z = [], [], []
    with open(datafile, 'r') as f:
        data = f.readlines()
        for i in range(7, len(data)):
            line = data[i].split()
            x.append(float(line[0]))
            y.append(float(line[1]))
            z.append(float(line[2]))
        if 0 < max(z) < 45:
            c = 'r'
        elif 45 < max(z) < 49:
            c = 'g'
        else:
            c = 'b'
    ax.plot(x, z, color=c)

plt.xlabel('X (nm)')
plt.ylabel('Z (nm)')
plt.gca().invert_yaxis()    
plt.show()