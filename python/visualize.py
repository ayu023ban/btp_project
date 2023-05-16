from matplotlib import pyplot as plt
from utils import get_3dfft
import numpy as np
from matplotlib import cm
from configuration import max_vel, Nr,  no_of_sensors, range_res, vel_res, max_range, no_of_channels, Nd
import signal
import torch
signal.signal(signal.SIGINT, signal.SIG_DFL)


def mango(sensor, channel, ax, complex=False):
    sensor = sensor.detach()
    Nr = sensor.shape[0]
    Nd = sensor.shape[1]
    Z = get_3dfft(sensor, complex=complex,device="cpu")
    s = Z[0:Nr//2, :, :]
    q = torch.tensor(np.zeros(s.shape), dtype=torch.cfloat).to(device="cpu")
    q[:, 0:Nd//2, :] = s[:, Nd//2:Nd, :]
    q[:, Nd//2:Nd, :] = s[:, 0:Nd//2, :]
    r =torch.abs(q)

    Z = r[:, :, channel]
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
        fig = plt.figure(figsize=(20,10))
        # fig.set_figheight(15)
        for channel in range(no_of_channels):
            ax1 = fig.add_subplot(2,no_of_channels,  
                                  channel + 1, projection='3d')
            ax1.title.set_text(f'input channel: {channel+1}')
            mango(input_sensor, channel, ax1)
            a = no_of_channels+channel + 1
            ax2 = fig.add_subplot(2,no_of_channels, a, projection='3d')
            ax2.title.set_text(f'output channel: {channel+1}')
            mango(output_sensor, channel, ax2)
        fig.suptitle(f"input and output of sensor: {index+1}")
        fig.tight_layout()
    plt.show()
