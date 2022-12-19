import os
import torch
from torch import nn
from WholeNetwork import WholeNetwork
from matplotlib import pyplot as plt
import time
from utils import get_output_path, get_3dfft
from visualize import heat_map
from configuration import no_of_channels, no_of_sensors, input_data

start_time = time.time()
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

no_of_epochs = 50
model = WholeNetwork(no_of_sensors).to(device)

# Adam Optimizer
learning_rate = 0.01
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
l1_bias = 0


def get_loss(outputs):
    matrix = []
    b = 0
    for x in outputs:
        z = get_3dfft(x)
        y = torch.reshape(z, (-1,))
        b += torch.norm(y, p=1)
        matrix.append(y)
    matrix = torch.stack(matrix)
    a = torch.norm(matrix, p=2, dim=0)
    a = torch.norm(a, p=1)
    c = a+l1_bias*b
    return c


def get_energy_of_diff_weight(initial_weights, final_weights):
    x = 0
    no_of_params = len(initial_weights)
    y = 0
    for index in range(no_of_params):
        x += torch.norm(initial_weights[index] -
                        final_weights[index], p=2)/torch.norm(initial_weights[index])
    return x


weight = model.get_weight_energy()
weight_energy_values = []
loss_values = []


final_output = None
inputs = None
for epoch_number in range(no_of_epochs):
    for sensor_data in input_data[:len(input_data)//100]:
        initial_weight_params = model.get_immutable_weights()
        optimizer.zero_grad()
        inputs = sensor_data.float()
        outputs = model.forward(sensor_data.float())
        final_output = outputs
        loss = get_loss(outputs)
        loss.backward()
        optimizer.step()
        loss_values.append(loss.item())
        final_weight_params = model.get_immutable_weights()
        energy_difference_weight = abs(get_energy_of_diff_weight(
            initial_weight_params, final_weight_params).item())
        weight_energy_values.append(energy_difference_weight)
        # print(final_weight_params[1])


plt.plot(loss_values)
plt.savefig(get_output_path("loss_figure.png"))
plt.clf()
plt.plot(weight_energy_values)
plt.savefig(get_output_path("energy_weight_difference.png"))
plt.clf()
print(f"Time elapsed: {time.time()-start_time}")


heat_map(inputs, final_output, 2)
