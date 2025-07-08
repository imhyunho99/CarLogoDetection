import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from ..models import Feedback, LogoLabel
from ..train import FeedbackDataset, transform  # 재사용
from .modelUtils import ResNet34
from .model_loader import device

def evaluate_model(model_path):
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        print("No labels found in DB. Cannot evaluate model.")
        return 0

    model = ResNet34(pretrained=False)
    model.model.fc = nn.Linear(512, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    dataset = FeedbackDataset(transform=transform)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=False)

    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    accuracy = correct / total if total > 0 else 0
    print(f"Evaluation accuracy of model {os.path.basename(model_path)}: {accuracy:.4f}")
    return accuracy


def replace_model_if_better(new_model_path, current_model_path, save_path):
    """
    새 모델과 기존 모델 평가해서 새 모델이 더 좋으면 교체 저장
    """
    new_acc = evaluate_model(new_model_path)
    current_acc = evaluate_model(current_model_path)

    if new_acc > current_acc:
        # 새 모델로 교체
        os.replace(new_model_path, save_path)
        print(f"Model updated. New accuracy {new_acc:.4f} > Current accuracy {current_acc:.4f}")
        return True
    else:
        # 성능 향상이 아니면 새 모델 삭제
        os.remove(new_model_path)
        print(f"Model not updated. Current accuracy {current_acc:.4f} >= New accuracy {new_acc:.4f}")
        return False
