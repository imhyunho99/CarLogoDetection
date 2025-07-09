import torch
from torch import nn
import torchvision.models as models
from ..models import LogoLabel

def get_label_list():
    return list(LogoLabel.objects.values_list('name', flat=True))


class ResNet34(nn.Module):
    def __init__(self, pretrained=True):
        super(ResNet34, self).__init__()

        label_list = get_label_list()
        self.class_num = len(label_list)

        if pretrained:
            self.model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
            print("Pretrained model loaded")
        else:
            self.model = models.resnet34(weights=None)
            print("Pretrained model loading failed, using untrained model")

        self.model.fc = nn.Linear(512, self.class_num)

    def forward(self, x):
        return self.model(x)  # 모델 그대로 사용 가능
