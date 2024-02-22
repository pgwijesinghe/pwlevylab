import matplotlib.pyplot as plt
import matplotlib.animation as animation

datafile = r'.\Casino_Plotter\data.dat'
savedir = r'.\Casino_Plotter\trajs'

def extract_trajectories(datafile, savedir):
    with open(datafile, 'r') as file:
        block_num = -1
        block_lines = []
        for line in file:
            flag = True if line.startswith('---') or line.startswith('\t---') else False
            if not flag:
                block_lines.append(line)
            if flag:
                with open(f'{savedir}\\block_{block_num}.txt', 'w') as block_file:
                    block_file.writelines(block_lines)
                block_num += 1
                block_lines = []

def plot_trajectories(savedir, animate=False):
    fig, ax = plt.subplots()
    ax.set_xlim(-80, 80)
    ax.set_ylim(0, 100)
    if animate:
        def update(frame):
            datafile = f'{savedir}\\block_{frame}.txt'
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

    else:
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
    if animate:
        ani = animation.FuncAnimation(fig, update, repeat=False, frames=500, interval=1)
        
    plt.xlabel('X (nm)')
    plt.ylabel('Z (nm)')
    plt.gca().invert_yaxis()    
    plt.show()

# extract_trajectories(datafile, savedir)
plot_trajectories(savedir, animate=True)