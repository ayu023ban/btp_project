import os
import torch
import numpy as np
import math
device = "cuda" if torch.cuda.is_available() else "cpu"

def dftmtx(N,device=device):
    return torch.tensor(np.fft.fft(np.eye(N)), dtype=torch.cfloat).to(device=device)


def get_output_path(filename):
    f = os.path.dirname(__file__) + f'/../output/{filename}'
    path = os.path.realpath(f)
    return path


def get_model_path():
    f = os.path.dirname(__file__) + '/model.pt'
    path = os.path.realpath(f)
    return path


def get_dataset_path(filename):
    f = os.path.dirname(__file__) + f'/../dataset/{filename}'
    path = os.path.realpath(f)
    return path


def get_3dfft(z, complex=False,device=device):
    Nr = z.shape[0]
    Nd = z.shape[1]
    Na = z.shape[2]
    Fr = dftmtx(Nr,device=device)/math.sqrt(Nr)
    Fd = dftmtx(Nd,device=device)/math.sqrt(Nd)
    Fa = dftmtx(Na,device=device)/math.sqrt(Na)
    y = torch.tensor(np.zeros([Nr, Nd, Na]), dtype=torch.cfloat).to(device=device)
    for channel in range(Na):
        temp = z[:, :, channel]
        Fd = torch.transpose(Fd, 0, 1)
        temp = torch.matmul(Fr, temp)
        temp = torch.matmul(temp, Fd)
        y[:, :, channel] = temp
    x = torch.tensor(np.zeros([Nr*Nd, Na]), dtype=torch.cfloat).to(device=device)
    for channel in range(Na):
        x[:, channel] = torch.reshape(y[:, :, channel], (Nr*Nd,))
    w = torch.matmul(x, torch.transpose(Fa, 0, 1))
    t = torch.tensor(np.zeros([Nr, Nd, Na]), dtype=torch.cfloat).to(device=device)
    for channel in range(Na):
        t[:, :, channel] = torch.reshape(w[:, channel], (Nr, Nd))
    # s = t[0:Nr//2, :, :]
    # q = torch.tensor(np.zeros(s.shape), dtype=torch.cfloat).to(device=device)
    # q[:, 0:Nd//2, :] = s[:, Nd//2:Nd, :]
    # q[:, Nd//2:Nd, :] = s[:, 0:Nd//2, :]
    # r =t.abs()
    return t


l1_bias = 0.0


def get_loss(outputs):
    matrix = []
    b = 0
    for x in outputs:
        z = get_3dfft(x,device=device)
        y = torch.reshape(z, (-1,))
        b += torch.norm(y, p=1)
        matrix.append(y)
    matrix = torch.stack(matrix)
    # temp = matrix[1,:] - matrix[0,:]
    # temp2 = torch.norm(temp,p=2)
    # return temp2
    a = torch.norm(matrix, p=2, dim=0)
    d = torch.norm(a, p=1)
    c = d+l1_bias*b
    return c


def get_energy_of_diff_weight(initial_weights, final_weights):
    x = 0
    no_of_params = len(initial_weights)
    y = 0
    for index in range(no_of_params):
        x += torch.norm(initial_weights[index] -
                        final_weights[index], p=2)/torch.norm(initial_weights[index])
    return x


def load_model(model, optimizer):
    path = get_model_path()
    if not os.path.exists(path):
        print("Model file not found so not able to load model")
        return
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])


def save_model(model, optimizer):
    path = get_model_path()
    torch.save({
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }, path)
