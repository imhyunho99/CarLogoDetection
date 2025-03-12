# 모델의 기존 구조 자체를 상속받아서 전이학습 하거나 VS 새로 선언해서 전이학습하거나. 근데 학습에 따라서 새로운 Class 추가가 가능함
import torch
from modelUtils import ResNet34
from torchvision.transforms import transforms


# 모델 불러오기
class LearnUtil:
    def __init__(self, model):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = ResNet34(pretrained=True).to(self.device)
