import torch
from torch import nn


class FeedForwardModel(nn.Module):
    def __init__(self, input_size):
        super(FeedForwardModel, self).__init__()

        # self.fc_layer1 = self._fc_layer_set(input_size, input_size//10)
        # self.fc_layer1 = self._fc_layer_set(input_size//10, input_size)
        self.net = nn.Sequential(
            nn.Linear(input_size, 100).to(torch.cfloat),
            nn.Linear(100, input_size).to(torch.cfloat),
            # nn.LeakyReLU(),
        )
        self.net.apply(self._init_weights)

    def phase_amplitude_relu(z):
        nn.Tanh()
        return Tanh(torch.abs(z)) * torch.exp(1.j * torch.angle(z))

    def _init_weights(self, module):
        if isinstance(module, nn.Embedding):
            module.weight.data.normal_(mean=0.0, std=1.0)
            if module.padding_idx is not None:
                module.weight.data[module.padding_idx].zero_()
        elif isinstance(module, nn.LayerNorm):
            module.bias.data.zero_()
            module.weight.data.fill_(1.0)
        elif isinstance(module, nn.Linear):
            torch.nn.init.zeros_(module.weight)
            module.bias.data.fill_(0.01)

    def _fc_layer_set(self, inp_dim, layer_dim):
        fc_layer = nn.Sequential(
            nn.Linear(inp_dim, layer_dim),
            nn.LeakyReLU(),
        )
        fc_layer = self.phase_amplitude_relu(fc_layer)
        return fc_layer

    def forward(self, x):
        a = x.shape
        b = x.shape[1:4]
        y = torch.complex(x[0], x[1])
        y = torch.flatten(y)
        z = y.cfloat()
        out = self.net(z)
        unflatten = nn.Unflatten(0, b)
        out = unflatten(out)
        return out
