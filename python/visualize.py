from matplotlib import pyplot as plt
from utils import get_3dfft
import torch
import numpy as np
from matplotlib import cm
from read_input import get_dataset


def heap_map(output, channel):
    data = get_dataset()
    max_vel = data['max_vel']
    max_range = data['max_range']
    Nr = data['Nr']
    Nd = data['Nd']
    for sensor in output:
        Z = get_3dfft(sensor)
        Z = Z[:, :, channel].detach()
        nx, ny = Z.shape[0], Z.shape[1]
        x = np.arange(-max_vel, max_vel, 2*max_vel/ny)
        y = np.arange(-(Nr/2), Nr/2, Nr/nx)
        hf = plt.figure()
        ha = plt.axes(projection='3d')
        X, Y = np.meshgrid(x, y)
        ha.plot_surface(X, Y, Z, cmap=cm.coolwarm)
        ha.view_init(azim=0, elev=90)
        plt.show()
