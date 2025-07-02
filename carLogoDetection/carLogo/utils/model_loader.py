import torch
from .modelUtils import ResNet34, LOGODICT

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
    model = ResNet34(pretrained=True).to(device)
    model.load_state_dict(torch.load("carLogo/model", map_location=device), strict=False)
    model.eval()
    return model, device, LOGODICT
