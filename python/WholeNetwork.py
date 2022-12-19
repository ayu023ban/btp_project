import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel
import copy

class WholeNetwork(nn.Module):
    def __init__(self, no_of_sensors):
        super(WholeNetwork, self).__init__()
        self.neural_networks = nn.ModuleList(
            [CNNModel() for x in range(no_of_sensors-1)])
        self.no_of_sensors = no_of_sensors

    def forward(self, sensor_data):
        out = []
        for index, l in enumerate(self.neural_networks):
            res = self.neural_networks[index].forward(sensor_data[index])
            out.append(res)
        out.append(sensor_data[self.no_of_sensors-1])
        return out

    def get_weight_energy(self):
        x = 0
        for params in self.parameters():
            x += torch.norm(params, p=2)
        return x

    def get_immutable_weights(self):
        x = []
        for param in self.parameters():
            x.append(param.detach().clone())
        y = copy.deepcopy(x)
        return y
