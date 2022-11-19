import os
import torch

def get_output_path(filename):
    f = os.path.dirname(__file__)+ f'/../output/{filename}'
    path = os.path.realpath(f)
    return path

def get_3dfft(x):
    z = torch.complex(x[0], x[1])
    z = torch.fft.fftn(z)
    z = torch.fft.fftshift(z)
    z = z.abs()
    return z