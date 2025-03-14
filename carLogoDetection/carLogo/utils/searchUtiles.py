import torch
from modelUtils import ResNet34
from torchvision.transforms import transforms


# 모델 불러오기
class SearchUtil:
    def __init__(self, model):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = ResNet34(pretrained=True).to(self.device)

    def search(self, image):
        self.model.load_state_dict(torch.load("model"))  # 학습한 모델 사용
        trans = transforms.Compose(
            [
                transforms.Resize((224, 224)),  # 이미지 크기 조정
                transforms.ToTensor(),  # 이미지를 텐서로 변환
            ]
        )
        # 새로운 이미지 로드 및 전처리
        input_image = trans(image).unsqueeze(0)
        # 모델 입력 및 예측
        output = self.model(input_image)
        # 예측 결과 확인
        # agrmax 값이 너무 작으면 Alert 예측값이 너무 작습니다. 학습되지 않은 로고일 수 있습니다. 라벨을 입력하세욘 추가개발
        predicted_label = torch.argmax(output)

        return predicted_label
