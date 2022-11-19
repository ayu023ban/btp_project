import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from CNNModel import CNNModel
from read_input import get_dataset
from WholeNetwork import WholeNetwork
from matplotlib import pyplot as plt
import time
from utils import get_output_path, get_3dfft
from visualize import visualize, heap_map

start_time = time.time()
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

data = get_dataset()
data = data['data']
x_data = torch.from_numpy(data)

no_of_sensors = data.shape[1]

# Definition of hyperparameters
n_iters = 4500
# num_epochs = n_iters / (len(train_x) / batch_size)
# num_epochs = int(num_epochs)

model = WholeNetwork(no_of_sensors).to(device)

# Adam Optimizer
learning_rate = 0.01
# print(model.parameters)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


def get_loss(outputs):
    matrix = []
    for x in outputs:
        z = get_3dfft(x)
        y = torch.reshape(x, (-1,))
        matrix.append(y)
    matrix = torch.stack(matrix)
    a = torch.norm(matrix, p=2, dim=0)
    a = torch.norm(a, p=1)
    return a


def get_energy_of_diff_weight(initial_weights, final_weights):
    x = 0
    no_of_params = len(initial_weights)
    for index in range(no_of_params):
        x += torch.norm(initial_weights[index] -
                        final_weights[index], p=2)
    return x


weight = model.get_weight_energy()
weight_energy_values = []
loss_values = []

final_output = None

for sensor_data in x_data[:len(x_data)//100]:
    initial_weight_params = model.get_immutable_weights()
    optimizer.zero_grad()
    outputs = model.forward(sensor_data.float())
    final_output = outputs
    loss = get_loss(outputs)
    loss.backward()
    optimizer.step()
    final_weight_params = model.get_immutable_weights()
    energy_difference_weight = abs(get_energy_of_diff_weight(
        initial_weight_params, final_weight_params).item())
    weight_energy_values.append(energy_difference_weight)
    loss_values.append(loss.item())

heap_map(final_output, 2)

# plt.plot(loss_values)
# plt.savefig(get_output_path("loss_figure.png"))
# plt.plot(weight_energy_values)
# plt.savefig(get_output_path("energy_weight_difference.png"))
print(f"Time elapsed: {time.time()-start_time}")
