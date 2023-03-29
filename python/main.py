import os
import torch
from torch import nn
from WholeNetwork import WholeNetwork
from matplotlib import pyplot as plt
import time
from utils import get_output_path, get_loss, get_energy_of_diff_weight, load_model
from visualize import heat_map
from configuration import no_of_sensors, input_data, sensor_dimension
from read_input import  get_model_path

start_time = time.time()
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

no_of_epochs = 1
model = WholeNetwork(no_of_sensors, sensor_dimension).to(device)
input_data = input_data.to(device)

# Adam Optimizer
learning_rate = 0.1
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# load_model(model,optimizer)

weight_energy_values = []
loss_values = []


final_output = None
inputs = None
count = 0


wei = []
for sensor_data in input_data[1:len(input_data)//100]:
    for epoch_number in range(no_of_epochs):
        count += 1
        initial_weight_params = model.get_immutable_weights()
        optimizer.zero_grad()
        inputs = sensor_data.float()
        outputs = model.forward(sensor_data.float())
        final_output = outputs
        loss = get_loss(outputs)
        # loss = 
        # print(loss.grad)
        loss.backward()
        if count%1000==0:
            for param in model.neural_networks[0].fc_layer1.parameters():
                print(param[10,10])
                print(param.grad[10,10])
                print('\n')
                break
        # print(model.neural_networks[0].fc_layer2.weight.grad[10,10])
        optimizer.step()
        # for param in model.neural_networks[0].fc_layer2.parameters():
        #     print(param[10,10])
        #     break
        # print("\n")
        # print(loss.grad)
        loss_values.append(loss.item())
        final_weight_params = model.get_immutable_weights()
        energy_difference_weight = abs(get_energy_of_diff_weight(
            initial_weight_params, final_weight_params).item())
        weight_energy_values.append(energy_difference_weight)
        if count % 1000 == 0:
            print(f"Iteration: {count}, loss: {loss.item()}")


# plt.plot(wei)
# plt.savefig(get_output_path("wei.png"))
# plt.clf()
plt.plot(loss_values)
plt.savefig(get_output_path("loss_figure.png"))
plt.clf()
plt.plot(weight_energy_values)
# plt.savefig(get_output_path("energy_weight_difference.png"))
# plt.clf()
# plt.close()
print(f"Time elapsed: {time.time()-start_time}")

traced_model = torch.jit.trace(model.forward,inputs)
torch.jit.save(traced_model,get_model_path())

inputs_cpu = inputs.cpu()
final_output_cpu = final_output.cpu()

heat_map(inputs_cpu, final_output_cpu, 2)
