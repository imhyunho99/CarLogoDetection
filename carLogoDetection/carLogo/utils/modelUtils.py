import torch
from torch import nn
import torchvision.models as models

LOGODICT = [
    "acura",
    "alfaromeo",
    "buick",
    "cadillac",
    "dodge",
    "fiat",
    "hyundai",
    "lexus",
    "mazda",
    "mercedes",
    "opel",
    "skoda",
    "toyota",
    "volkswagen",
]


class ResNet34(nn.Module):
    def __init__(self, pretrained=True):
        super(ResNet34, self).__init__()

        self.class_num = len(LOGODICT)

        if pretrained:
            self.model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
            print("Pretrained model loaded")
        else:
            self.model = models.resnet34(weights=None)
            print("Pretrained model loading failed, using untrained model")

        # **🔥 기존 fc (1000개 클래스) → 7개 클래스 변경**
        self.model.fc = nn.Linear(512, self.class_num)

    def forward(self, x):
        return self.model(x)  # 모델 그대로 사용 가능
