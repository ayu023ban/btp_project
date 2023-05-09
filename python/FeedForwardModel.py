import torch
from torch import nn


class FeedForwardModel(nn.Module):
    def __init__(self, input_size):
        super(FeedForwardModel, self).__init__()

        self.fc_layer1 = self._fc_layer_set(input_size, 50)
        self.fc_layer2 = self._fc_layer_set(50,50)
        self.fc_layer3 = self._fc_layer_set(50,50)
        # self.fc_layer4 = self._fc_layer_set(50,50)
        self.fc_layer5 = self._fc_layer_set(50,input_size)
        # self.net = nn.Sequential(
        #     nn.Linear(input_size, 100).to(torch.cfloat),
        #     nn.Linear(100, 100).to(torch.cfloat),
        #     nn.Linear(100, input_size).to(torch.cfloat),
        #     # nn.LeakyReLU(),
        # )
    
    def net(self,z):
        out = self.fc_layer1(z)
        out = self.phase_amplitude_relu(out)
        out = self.fc_layer2(out)
        out = self.phase_amplitude_relu(out)
        out = self.fc_layer3(out)
        out = self.phase_amplitude_relu(out)
        # out = self.fc_layer4(out)
        # out = self.phase_amplitude_relu(out) 
        out = self.fc_layer5(out)
        out = self.phase_amplitude_relu(out)
        return out

    def phase_amplitude_relu(self, z):
        c = torch.abs(z)
        tanh = nn.Tanh()
        a = tanh(c)
        b = torch.exp( (1j)* torch.angle(z))
        return torch.mul(a,b)

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
        fc_layer = nn.Linear(inp_dim,layer_dim).to(torch.cfloat)
        return fc_layer

    def forward(self, x):
        b = x.shape
        y = torch.flatten(x)
        z = y.cfloat()
        out = self.net(z)
        out = out.view(b)
        return out
