import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")


class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()

        self.conv_layer1 = self._conv_layer_set(3, 32)
        self.conv_layer2 = self._conv_layer_set(32, 64)
        self.fc1 = nn.Linear(2**3*64, 128)
        self.fc2 = nn.Linear(128, num_classes)
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
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.batch(out)
        out = self.drop(out)
        out = self.fc2(out)

        return out


class WholeNetwork(nn.Module):
    def __init__(self,no_of_sensors):
        self.neural_networks = [CNNModel() for x in range(no_of_sensors)]
        self.no_of_sensors = no_of_sensors
    
    def forward(self,sensor_data):
        out = []
        for index in range(self.no_of_sensors):
            res = self.neural_networks[index].forward(sensor_data[index])
            out.append(res)
        return out
    
#Definition of hyperparameters
n_iters = 4500
num_epochs = n_iters / (len(train_x) / batch_size)
num_epochs = int(num_epochs)

# Create CNN
model = WholeNetwork(5)
#model.cuda()
print(model)

# Cross Entropy Loss 
error = nn.CrossEntropyLoss()

# SGD Optimizer
learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
data = []

def error(outputs):
    pass

for sensor_data in data:
    optimizer.zero_grad()
    outputs = model(sensor_data)
    loss = error(outputs)
    # Calculating gradients
    loss.backward()
    # Update parameters
    optimizer.step()
    