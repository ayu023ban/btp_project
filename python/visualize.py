from matplotlib import pyplot as plt
from utils import get_3dfft
import numpy as np
from matplotlib import cm
from configuration import max_vel, Nr,  no_of_sensors, range_res, vel_res, max_range, no_of_channels
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)


def mango(sensor, channel, ax, complex=False):
    Z = get_3dfft(sensor, complex=complex)
    Z = Z[:, :, channel].detach()
    nx, ny = Z.shape[0], Z.shape[1]
    x = np.arange(-max_vel, max_vel, vel_res)
    y = np.arange(0, max_range, range_res)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.view_init(azim=0, elev=90)
    ax.set(
        xlabel='Speed',
        ylabel='Range',
        zlabel='Amplitude',
    )


def heat_map(input_sensors, output_sensors):
    for index in range(no_of_sensors-1):
        input_sensor = input_sensors[index]
        output_sensor = output_sensors[index]
        fig = plt.figure(figsize=plt.figaspect(2))
        for channel in range(no_of_channels):
            ax1 = fig.add_subplot(no_of_channels, 2, 2 *
                                  channel + 1, projection='3d')
            mango(input_sensor, channel, ax1)
            ax2 = fig.add_subplot(no_of_channels, 2, 2 *
                                  channel + 2, projection='3d')
            mango(output_sensor, channel, ax2)
        fig.suptitle(f"input and output of sensor: {index+1}")
    plt.show()
