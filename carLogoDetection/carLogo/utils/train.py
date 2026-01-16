import sys
import os
import django

# BASE_DIR = ~/carlogo/CarLogoDetection
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carLogoDetection.settings")
django.setup()

import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from ..models import Feedback, LogoLabel
from .modelUtils import ResNet34
from .model_loader import device, MODEL_PATH
from tqdm import tqdm
from sklearn.model_selection import train_test_split

BATCH_SIZE = 8
EPOCHS = 5
LR = 1e-4

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'media')


class FeedbackDataset(Dataset):
    def __init__(self, feedbacks, transform=None):
        self.feedbacks = feedbacks
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


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


import logging

logger = logging.getLogger('training')

# ... (rest of the imports)

# ... (FeedbackDataset class)

def train():
    num_classes = LogoLabel.objects.count()
    if num_classes == 0:
        logger.warning("No labels found in DB. Aborting training.")
        return

    all_feedbacks = list(Feedback.objects.all())
    train_feedbacks, val_feedbacks = train_test_split(all_feedbacks, test_size=0.2, random_state=42)

    train_dataset = FeedbackDataset(train_feedbacks, transform=transform)
    val_dataset = FeedbackDataset(val_feedbacks, transform=transform)

    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = ResNet34()
    # Load the state dict from the current model
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        logger.info(f"Loaded weights from {MODEL_PATH} for fine-tuning.")
    
    model.model.fc = nn.Linear(512, num_classes)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    model.train()
    for epoch in range(EPOCHS):
        total_loss = 0.0
        for images, labels in tqdm(train_dataloader, desc=f"Epoch {epoch + 1}/{EPOCHS}"):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_dataloader)
        logger.info(f"Epoch {epoch + 1} average loss: {avg_loss:.4f}")

    retrained_model_path = MODEL_PATH.parent / "model_retrained.pt"
    torch.save(model.state_dict(), retrained_model_path)
    logger.info(f"Retrained model saved to {retrained_model_path}")

    # Return validation dataloader for evaluation
    return val_dataloader


if __name__ == "__main__":
    train()
