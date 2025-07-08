import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from .models import Feedback, LogoLabel
from utils.modelUtils import ResNet34
from utils.model_loader import device
from tqdm import tqdm

BATCH_SIZE = 8
EPOCHS = 5
LR = 1e-4

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'media')


class FeedbackDataset(Dataset):
    def __init__(self, transform=None):
        self.feedbacks = list(Feedback.objects.all())
        self.transform = transform

        labels = LogoLabel.objects.all()
        self.label2idx = {label.name: idx for idx, label in enumerate(labels)}

    def __len__(self):
        return len(self.feedbacks)

    def __getitem__(self, idx):
        feedback = self.feedbacks[idx]
        image_path = os.path.join(MEDIA_ROOT, feedback.image.name)
        image = Image.open(image_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        label_idx = self.label2idx.get(feedback.correct_label, -1)
        if label_idx == -1:
            raise ValueError(f"Unknown label: {feedback.correct_label}")

        return image, label_idx


# 이미지 전처리 (train)
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


def train():
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        print("No labels found in DB. Aborting training.")
        return

    model = ResNet34(pretrained=False)
    model.model.fc = nn.Linear(512, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    dataset = FeedbackDataset(transform=transform)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0.0
        for images, labels in tqdm(dataloader, desc=f"Epoch {epoch + 1}/{EPOCHS}"):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1} average loss: {avg_loss:.4f}")

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_retrained.pt")
    torch.save(model.state_dict(), save_path)
    print(f"Retrained model saved to {save_path}")


if __name__ == "__main__":
    train()
