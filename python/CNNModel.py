from torch import nn


class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()

        self.conv_layer1 = self._conv_layer_set(2, 2)
        self.conv_layer2 = self._conv_layer_set(2, 2)

    def _conv_layer_set(self, in_c, out_c):
        conv_layer = nn.Sequential(
            nn.Conv3d(in_c, out_c, kernel_size=(
                21, 21, 3), padding=(10, 10, 1)),
            nn.LeakyReLU(),
        )
        return conv_layer

    def forward(self, x):
        out = self.conv_layer1(x)
        out = self.conv_layer2(out)
        # out = self.conv_layer3(out)
        # out = self.conv_layer4(out)
        # out = self.conv_layer5(out)
        return out
