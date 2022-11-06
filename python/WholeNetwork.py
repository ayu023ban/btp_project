import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel

class WholeNetwork(nn.Module):
    def __init__(self, no_of_sensors):
        super(WholeNetwork, self).__init__()
        self.neural_networks = nn.ModuleList([CNNModel() for x in range(no_of_sensors)])
        self.no_of_sensors = no_of_sensors

    def forward(self, sensor_data):
        out = []
        for index, l in enumerate(self.neural_networks):
            res = self.neural_networks[index].forward(sensor_data[index])
            out.append(res)
        return out