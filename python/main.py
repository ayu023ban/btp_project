import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel
from read_input import get_dataset
from WholeNetwork import WholeNetwork

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")


# Definition of hyperparameters
n_iters = 4500
# num_epochs = n_iters / (len(train_x) / batch_size)
# num_epochs = int(num_epochs)

# Create CNN
model = WholeNetwork(2)
# model.cuda()
# print(model)

# Cross Entropy Loss
error = nn.CrossEntropyLoss()

# SGD Optimizer
learning_rate = 0.001
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
data = get_dataset()
data = data['data']
x_data = torch.from_numpy(data)

def get_loss(outputs):
    matrix = []
    for x in outputs:
        y = torch.reshape(x,(2,-1,))
        y = torch.norm(y,p=2,dim=0)
        matrix.append(y)
    matrix = torch.stack(matrix)
    a = torch.norm(matrix,p=2,dim=0)
    a = torch.norm(a,p=1)
    return a


for sensor_data in x_data[:len(x_data)//10]:
    optimizer.zero_grad()
    outputs = model.forward(sensor_data.float())
    loss = get_loss(outputs)
    # Calculating gradients
    loss.backward()
    # Update parameters
    optimizer.step()
