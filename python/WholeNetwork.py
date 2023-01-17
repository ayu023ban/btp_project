import os
import torch
from torch import nn
from CNNModel import CNNModel
from FeedForwardModel import FeedForwardModel
import copy
from utils import get_model_path

class WholeNetwork(nn.Module):
    def __init__(self, no_of_sensors, input_size, load=False):
        super(WholeNetwork, self).__init__()
        self.neural_networks = nn.ModuleList(
            [FeedForwardModel(input_size) for x in range(no_of_sensors-1)])
        self.no_of_sensors = no_of_sensors
        if load:
            self.load_state_dict(torch.load(get_model_path()))
    
    def forward(self, sensor_data):
        out = []
        for index, l in enumerate(self.neural_networks):
            res = self.neural_networks[index].forward(sensor_data[index])
            out.append(res)
        x = sensor_data[self.no_of_sensors-1]
        y = torch.complex(x[0], x[1])
        out.append(y)
        out = torch.stack(out)
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
