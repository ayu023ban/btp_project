from read_input import get_dataset
import torch
from WholeNetwork import WholeNetwork
from configuration import no_of_sensors,  sensor_dimension
import time
from utils import load_model
from scipy.io import savemat
from utils import get_dataset_path

start_time = time.time()
device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"
print(f"Using {device} device")

data = get_dataset("temp_input")
x_data= data['input']
input_data = torch.from_numpy(x_data)


model = WholeNetwork(no_of_sensors, sensor_dimension).to(device)
input_data = input_data.to(device)

# Adam Optimizer
learning_rate = 0.001
optimizer = torch.optim.Adam(
    model.parameters(), lr=learning_rate, weight_decay=0)

load_model(model, optimizer)

output = model.forward(input_data)
output_path = get_dataset_path('temp_output.mat')
with torch.no_grad():
    output_dict = {'output':output.cpu().numpy()}
    savemat(output_path,output_dict)
print(f"Time elapsed: {time.time()-start_time}")
