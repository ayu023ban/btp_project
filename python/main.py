import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel
from read_input import mat
from WholeNetwork import WholeNetwork

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")


# Definition of hyperparameters
n_iters = 4500
# num_epochs = n_iters / (len(train_x) / batch_size)
# num_epochs = int(num_epochs)

# Create CNN
model = WholeNetwork(5)
# model.cuda()
# print(model)

# Cross Entropy Loss
error = nn.CrossEntropyLoss()

# SGD Optimizer
learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
data = mat['data']
x_data = torch.from_numpy(data)
print(x_data.shape)

def error(outputs):
    pass


for sensor_data in x_data:
    optimizer.zero_grad()
    sensor_data = sensor_data[None, :, :, :]
    print(sensor_data.shape)
    outputs = model.forward(sensor_data)
    # loss = error(outputs)
    # # Calculating gradients
    # loss.backward()
    # # Update parameters
    # optimizer.step()
