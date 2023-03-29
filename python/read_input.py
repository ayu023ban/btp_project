import scipy.io
import os.path
import torch
from utils import get_model_path, get_dataset_path


# Generate Simulated Data of Sensors
# Output is 6D data with following information:
# 1st Index: Index of sample
# 2nd Index: Sensor Index
# 3rd Index: Dimension for storing real and imaginary values
# 4rd Index: Number of samples in one chirp
# 5th Index: chirps in one sequence
# 6th Index: Channel Index
def get_dataset(file_name):    
    path = get_dataset_path(file_name)
    mat = scipy.io.loadmat(path)
    return mat
