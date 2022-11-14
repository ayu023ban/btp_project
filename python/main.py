import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel
from read_input import get_dataset
from WholeNetwork import WholeNetwork
import matplotlib.pyplot as plt

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")


# Definition of hyperparameters
n_iters = 4500
# num_epochs = n_iters / (len(train_x) / batch_size)
# num_epochs = int(num_epochs)

model = WholeNetwork(2).to(device)

# Adam Optimizer
learning_rate = 0.01
# print(model.parameters)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

def get_loss(outputs):
    matrix = []
    for x in outputs:
        z = torch.complex(x[0],x[1])
        z = torch.fft.fftn(z)
        z = torch.fft.fftshift(z)
        z = z.abs()
        y = torch.reshape(x,(-1,))
        matrix.append(y)
    matrix = torch.stack(matrix)
    a = torch.norm(matrix,p=2,dim=0)
    a = torch.norm(a,p=1)
    return a

weight = model.get_weight_energy()
weight_energy_values = []
loss_values = []

data = get_dataset()
data = data['data']
x_data = torch.from_numpy(data)

for sensor_data in x_data[:len(x_data)]:
    initial_weight = model.get_weight_energy().item()
    optimizer.zero_grad()
    outputs = model.forward(sensor_data.float())
    loss = get_loss(outputs)
    loss.backward()
    optimizer.step()
    final_weight = model.get_weight_energy().item()
    weight_energy_values.append(abs(final_weight-initial_weight))
    loss_values.append(loss.item())

plt.plot(loss_values)
plt.show()
plt.plot(weight_energy_values)
plt.show()