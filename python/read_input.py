from utils import get_dataset_path
import mat73


# Generate Simulated Data of Sensors
# Output is 5D data with following information:
# 1st Index: Index of sample
# 2nd Index: Sensor Index
# 3rd Index: Number of samples in one chirp
# 4th Index: chirps in one sequence
# 5th Index: Channel Index
def get_dataset(file_name):
    path = get_dataset_path(file_name)
    mat = mat73.loadmat(path)
    return mat
