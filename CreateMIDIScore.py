import pypianoroll
import matplotlib.pyplot as plt

def create_score(path):
    multitrack = pypianoroll.read(path)
    multitrack.plot()
    #plt.show()
    fig_name = path[:-3] + 'png'
    plt.savefig(fig_name)
    
