import os
import torch
import numpy as np
import math


def dftmtx(N):
    return torch.tensor(np.fft.fft(np.eye(N)), dtype=torch.cfloat)


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


def get_3dfft(x, complex=False):
    z = x
    if (complex):
        z = torch.complex(x[0], x[1])
    # z = torch.fft.fftn(z)
    Nr = z.shape[0]
    Nd = z.shape[1]
    Na = z.shape[2]
    Fr = dftmtx(Nr)/math.sqrt(Nr)
    Fd = dftmtx(Nd)/math.sqrt(Nd)
    Fa = dftmtx(Na)/math.sqrt(Na)
    y = torch.tensor(np.zeros([Nr, Nd, Na]), dtype=torch.cfloat)
    for channel in range(Na):
        temp = z[:, :, channel]
        Fd = torch.transpose(Fd, 0, 1)
        temp = torch.matmul(Fr, temp)
        temp = torch.matmul(temp, Fd)
        y[:, :, channel] = temp
    x = torch.tensor(np.zeros([Nr*Nd, Na]), dtype=torch.cfloat)
    for channel in range(Na):
        x[:, channel] = torch.reshape(y[:, :, channel], (Nr*Nd,))
    w = torch.matmul(x, torch.transpose(Fa, 0, 1))
    t = torch.tensor(np.zeros([Nr, Nd, Na]), dtype=torch.cfloat)
    for channel in range(Na):
        t[:, :, channel] = torch.reshape(w[:, channel], (Nr, Nd))
    z = t[0:Nr//2, :, :]
    y = torch.tensor(np.zeros(z.shape), dtype=torch.cfloat)
    y[:, 0:Nd//2, :] = z[:, Nd//2:Nd, :]
    y[:, Nd//2:Nd, :] = z[:, 0:Nd//2, :]
    z = y.abs()
    return z


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
