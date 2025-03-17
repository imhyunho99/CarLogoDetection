import pretrainedmodels
import torch
from torch import nn
import torch.nn.functional as F


MODEL_PATH = "carLogoDetection/carLogo/model"
LOGODICT = ["acura", "alfaromeo", "buick", "cadillac", "dodge", "fiat", "opel"]


class ResNet34(nn.Module):

    def __init__(self, pretrained):
        super(ResNet34, self).__init__()
        self.class_num = 7
        if pretrained is True:
            self.model = pretrainedmodels.__dict__["resnet34"](pretrained="imagenet")
        else:
            self.model = pretrainedmodels.__dict__["resnet34"](pretrained=None)

        # change the classification layer
        self.l0 = nn.Linear(512, self.class_num)
        self.dropout = nn.Dropout2d(0.6)

    def forward(self, x):
        # get the batch size only, ignore (c, h, w)
        batch, _, _, _ = x.shape
        x = self.model.features(x)
        x = F.adaptive_avg_pool2d(x, 1).reshape(batch, -1)
        x = self.dropout(x)
        l0 = self.l0(x)
        return l0
