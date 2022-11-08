import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()

        self.conv_layer1 = self._conv_layer_set(2, 2)
        self.conv_layer2 = self._conv_layer_set(2, 2)
        # self.fc1 = nn.Linear(2**3*64, 128)
        # self.fc2 = nn.Linear(128, 5)
        self.relu = nn.LeakyReLU()
        self.batch = nn.BatchNorm1d(128)
        self.drop = nn.Dropout(p=0.15)

    def _conv_layer_set(self, in_c, out_c):
        conv_layer = nn.Sequential(
            nn.Conv3d(in_c, out_c, kernel_size=(3, 3, 3), padding=0),
            nn.LeakyReLU(),
            nn.MaxPool3d((2, 2, 2)),
        )
        return conv_layer

    def forward(self, x):
        # Set 1
        out = self.conv_layer1(x)
        out = self.conv_layer2(out)
        # out = out.view(out.size(0), -1)
        # out = self.fc1(out)
        # out = self.relu(out)
        # out = self.batch(out)
        # out = self.drop(out)
        # out = self.fc2(out)

        return out
