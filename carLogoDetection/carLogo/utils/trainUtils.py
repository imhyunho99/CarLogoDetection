import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from ..models import LogoLabel
from .train import FeedbackDataset, transform
from .modelUtils import ResNet34
from .model_loader import device

def evaluate_model(model_path):
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        print("No labels found in DB. Cannot evaluate model.")
        return 0

    model = ResNet34(pretrained=False).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
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

def train_model(train_dataset, epochs=5, batch_size=8, lr=0.001):
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        print("No labels found in DB. Cannot train model.")
        return None

    model = ResNet34(pretrained=False).to(device)
    model.train()

    dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in dataloader:
            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")

    # 학습 후 체크포인트 저장
    save_path = "carLogo/models/model_retrained.pt"
    torch.save(model.state_dict(), save_path)
    print(f"Retrained model saved to {save_path}")
    return save_path

def replace_model_if_better(new_model_path, current_model_path, save_path):
    new_acc = evaluate_model(new_model_path)
    current_acc = evaluate_model(current_model_path)

    if new_acc > current_acc:
        os.replace(new_model_path, save_path)
        print(f"Model updated. New accuracy {new_acc:.4f} > Current accuracy {current_acc:.4f}")
        return True
    else:
        os.remove(new_model_path)
        print(f"Model not updated. Current accuracy {current_acc:.4f} >= New accuracy {new_acc:.4f}")
        return False
