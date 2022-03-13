import matplotlib.pyplot as plt

def plot_dist(nlines, nchars, nwords, nnodes):
    y1, y2, y3, x = nlines, nchars, nwords, nnodes
    fig, axs = plt.subplots(nrows=1,ncols=3)
    axs[0].set_ylabel('nnodes')
    axs[0].plot(y1, x, 'o')
    axs[0].set_xlabel('Nlines')
    axs[1].plot(y2, x, 'o')
    axs[1].set_xlabel('Nchars')
    axs[2].plot(y3, x, 'o')
    axs[2].set_xlabel('Nwords')
    plt.show()

