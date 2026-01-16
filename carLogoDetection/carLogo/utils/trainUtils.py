import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from ..models import LogoLabel
from .train import FeedbackDataset, transform
from .modelUtils import ResNet34
from .model_loader import device
import logging

logger = logging.getLogger('training')

def evaluate_model(model_path, val_dataloader):
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        logger.warning("No labels found in DB. Cannot evaluate model.")
        return 0

    model = ResNet34(pretrained=False).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in val_dataloader:
            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)
            _, preds = torch.max(outputs, 1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    accuracy = correct / total if total > 0 else 0
    logger.info(f"Evaluation accuracy of model {os.path.basename(model_path)}: {accuracy:.4f}")
    return accuracy

def replace_model_if_better(new_model_path, current_model_path, save_path, val_dataloader):
    new_acc = evaluate_model(new_model_path, val_dataloader)
    current_acc = evaluate_model(current_model_path, val_dataloader)

    if new_acc > current_acc:
        os.replace(new_model_path, save_path)
        logger.info(f"Model updated. New accuracy {new_acc:.4f} > Current accuracy {current_acc:.4f}")
        return True
    else:
        os.remove(new_model_path)
        logger.info(f"Model not updated. Current accuracy {current_acc:.4f} >= New accuracy {new_acc:.4f}")
        return False
