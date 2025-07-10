import os
import torch
from .modelUtils import ResNet34, get_label_list

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_PATH = "carLogo/models/model_current.pt"

def load_model():
    # DB에서 클래스 수를 확인해 pretrained 모델 생성
    model = ResNet34(pretrained=True).to(device)

    if os.path.exists(MODEL_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device), strict=False)
            print(f"Loaded model checkpoint from {MODEL_PATH}")
        except Exception as e:
            print(f"Failed to load checkpoint, using pretrained model. Error: {e}")
    else:
        # 체크포인트 없으면 처음 pretrained 모델 저장
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Saved initial pretrained model checkpoint to {MODEL_PATH}")

    model.eval()
    return model, device, get_label_list()
