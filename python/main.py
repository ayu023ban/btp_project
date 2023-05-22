import torch
from WholeNetwork import WholeNetwork
from matplotlib import pyplot as plt
import time
start_time = time.time()
from utils import get_output_path, get_loss, get_energy_of_diff_weight
from visualize import heat_map
from configuration import no_of_sensors, input_data, sensor_dimension, ground_target_coordinates, ground_target_velocities


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

no_of_epochs = 2
model = WholeNetwork(no_of_sensors, sensor_dimension).to(device)
print(model.eval())

input_data = input_data.to(device)

# Adam Optimizer
learning_rate = 1
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# load_model(model, optimizer)

weight_energy_values = []
loss_values = []


final_output = None
inputs = None
count = 0
counts = []
print("input length: ", len(input_data))
sensor_to_plot = 13
# idx = torch.randperm(input_data.shape[0])
# input_data=input_data[idx,:,:,:,:]
for epoch_number in range(no_of_epochs):
    for sensor_data in input_data[0:len(input_data)]:
        count += 1
        initial_weight_params = model.get_immutable_weights()
        optimizer.zero_grad()
        outputs = model.forward(sensor_data.cfloat())
        if count == sensor_to_plot:
            inputs = sensor_data.cfloat()
            ground_truth = {
                "position": ground_target_coordinates[sensor_to_plot-1],
                "velocity": ground_target_velocities[sensor_to_plot-1]
            }
            final_output = outputs
        loss = get_loss(outputs)
        # print(loss.grad)
        loss.backward()
        # if count % 30 == 0:
        #     for param in model.neural_networks[0].fc_layer1.parameters():
        #         print(param[10, 10])
        #         print(param.grad[10, 10])
        #         print('\n')
        #         break
        optimizer.step()
        # for param in model.neural_networks[0].fc_layer2.parameters():
        #     print(param[10,10])
        #     break
        # print("\n")
        # print(loss.grad)
        
        final_weight_params = model.get_immutable_weights()
        energy_difference_weight = abs(get_energy_of_diff_weight(
            initial_weight_params, final_weight_params).item())
        weight_energy_values.append(energy_difference_weight)
        loss_values.append(loss.item())
        counts.append(count)
        if count %100 == 0:
            print(f"Iteration: {count}, loss: {loss.item()}")

# plt.plot(wei)
# plt.savefig(get_output_path("wei.png"))
# plt.clf()
xi = list(range(len(counts)))
plt.plot(counts,loss_values)
plt.xlabel('Number of Iterations')
plt.ylabel('Loss')
plt.title('Loss Figure')
plt.savefig(get_output_path("loss_figure.png"))
plt.clf()
# plt.plot(weight_energy_values)
# plt.savefig(get_output_path("energy_weight_difference.png"))
# plt.clf()
plt.close()
print(f"Time elapsed: {time.time()-start_time}")
# save_model(model, optimizer)
inputs_cpu = inputs.cpu()
final_output_cpu = final_output.cpu()
print(ground_truth)
heat_map(inputs_cpu, final_output_cpu)
