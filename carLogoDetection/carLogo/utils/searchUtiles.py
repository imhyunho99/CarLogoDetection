import torch

from .modelUtils import ResNet34
from . import imageUtils
from . import modelUtils
from torchvision.transforms import transforms


# 모델 불러오기
def setDevice():
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def setModel():
    return ResNet34(pretrained=True).to()


def search(image):
    device = setDevice()
    model = setModel().to(device)
    image = imageUtils.in_memory_file_to_pil(image)

    model.load_state_dict(torch.load("carLogo/model"), strict=False)  # 학습한 모델 사용

    trans = transforms.Compose(
        [
            transforms.Resize((224, 224)),  # 이미지 크기 조정
            transforms.ToTensor(),  # 이미지를 텐서로 변환
        ]
    )

    # 새로운 이미지 로드 및 전처리
    input_image = trans(image).unsqueeze(0)
    # 모델 입력 및 예측
    output = model(input_image)
    # 예측 결과 확인
    # agrmax 값이 너무 작으면 Alert 예측값이 너무 작습니다. 학습되지 않은 로고일 수 있습니다. 라벨을 입력하세욘 추가개발

    output = output.softmax(dim=1)
    print(output)
    predicted_label = modelUtils.LOGODICT[output.argmax(dim=1).item()]  # 예측된 라
    print(predicted_label)
    return predicted_label
