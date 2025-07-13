import os
import torch
from .modelUtils import ResNet34, get_label_list

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_PATH = "carLogo/models/model_current.pt"

def load_model():
    model = ResNet34(pretrained=True).to(device)

    if os.path.exists(MODEL_PATH):
        try:
            model.load_state_dict(torch.load(MODEL_PATH, map_location=device), strict=False)
            print(f"Loaded model checkpoint from {MODEL_PATH}")
        except Exception as e:
            print(f"Failed to load checkpoint, using pretrained model. Error: {e}")
    else:
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Saved initial pretrained model checkpoint to {MODEL_PATH}")

    model.eval()
    return model, device, get_label_list()
