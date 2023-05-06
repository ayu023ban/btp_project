from matplotlib import pyplot as plt
from utils import get_3dfft
import numpy as np
from matplotlib import cm
from configuration import  max_vel, Nr,  no_of_sensors
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


def mango(sensor, channel, ax, complex=False):
    Z = get_3dfft(sensor, complex=complex)
    Z = Z[:, :, channel].detach()
    nx, ny = Z.shape[0], Z.shape[1]
    x = np.arange(-max_vel, max_vel, 2*max_vel/ny)
    y = np.arange(-(Nr/2), Nr/2, Nr/nx)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.view_init(azim=0, elev=90)
    ax.set(
        xlabel='Speed',
        ylabel='Range',
        zlabel='Amplitude',
    )


def heat_map(input, output, channel):
    for index in range(no_of_sensors-1):
        input_sensor = input[index]
        output_sensor = output[index]
        fig = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig.add_subplot(1, 2, 1, projection='3d')
        mango(input_sensor, channel, ax1, complex=False)
        ax2 = fig.add_subplot(1, 2, 2, projection='3d')
        mango(output_sensor, channel, ax2)
        fig.suptitle(f"input and output of sensor: {index+1}")
    plt.show()
