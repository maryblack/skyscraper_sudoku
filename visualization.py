import numpy as np
import matplotlib.pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def plot_city(solution: list):
    fig = plt.figure(figsize=(7, 7))
    ax1 = fig.add_subplot(111, projection='3d')

    _x = np.arange(6)
    _y = np.arange(6)
    _xx, _yy = np.meshgrid(_x, _y)
    x, y = _xx.ravel(), _yy.ravel()

    top = np.array(solution)
    bottom = np.zeros_like(top)
    width = depth = 1

    cmap = plt.cm.viridis(plt.Normalize(0, 6)(top))

    ax1.bar3d(x, y, bottom, width, depth, top, shade=True, color=cmap)
    ax1.set_title('Skyscrapers')
    # plt.savefig('city.png')

    plt.show()