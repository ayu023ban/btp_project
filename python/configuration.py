import torch
from read_input import get_dataset


data = get_dataset('training_dataset.mat')
max_vel = data['max_vel']
max_range = data['max_range']
Nr = data['Nr']
Nd = data['Nd']
no_of_channels = data['no_of_channels']
x_data = data['output']
input_data = torch.from_numpy(x_data)
no_of_sensors = x_data.shape[1]

t = x_data.shape
sensor_dimension = t[2]*t[3]*t[4]

manual_channels = 4
manual_sensors = 2

no_of_channels = min(no_of_channels, manual_channels)
no_of_sensors = min(no_of_sensors, manual_sensors)

if (no_of_channels < manual_channels):
    print("manual channels is more than channels in data")
if (no_of_sensors < manual_sensors):
    print("manual sensors is more than sensors in data")
