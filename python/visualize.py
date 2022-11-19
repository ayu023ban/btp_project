from matplotlib import pyplot as plt
from utils import get_3dfft
import torch
import numpy as np
from matplotlib import cm


def visualize(data, channel):
    for sensor in data:
        Z = get_3dfft(sensor)
        Z = Z[:, :, channel].detach()
        nx, ny = Z.shape[0], Z.shape[1]
        x = np.arange(-100, 100, 200/ny)
        y = np.arange(-60, 60, 120/nx)
        hf = plt.figure()
        ha = plt.axes(projection='3d')
        X, Y = np.meshgrid(x, y)
        ha.plot_surface(X, Y, Z, cmap=cm.coolwarm)
        plt.show()


def heap_map(data, channel):
    for sensor in data:
        Z = get_3dfft(sensor)
        Z = Z[:, :, channel].detach()
        # fig, ax = plt.subplots(figsize=(5,5))
        # im = ax.imshow(Z, cmap='hot', interpolation='nearest')
        # nx, ny = Z.shape[0], Z.shape[1]
        # x = np.arange(-100, 100, 200/ny)
        # y = np.arange(-60, 60, 120/nx)
        # ax.set_xticks(x,size=10)
        # ax.set_yticks(y,size=10)
        # plt.show()
        nx, ny = Z.shape[0], Z.shape[1]
        x = np.arange(-100, 100, 200/ny)
        y = np.arange(-60, 60, 120/nx)
        hf = plt.figure()
        ha = plt.axes(projection='3d')
        X, Y = np.meshgrid(x, y)
        ha.plot_surface(X, Y, Z, cmap=cm.coolwarm)
        ha.view_init(azim=0, elev=90)
        plt.show()
