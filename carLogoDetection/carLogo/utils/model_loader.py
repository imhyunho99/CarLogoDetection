import os
import torch
from .modelUtils import ResNet34, get_label_list
import logging

from pathlib import Path

logger = logging.getLogger('deployment')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "carLogo/models/model_current.pt"

def load_model():
    # Get label list first to determine output size
    label_dict = get_label_list()
    num_classes = len(label_dict) if label_dict else 14  # Default to 14 if no labels
    
    model = ResNet34().to(device)

    if os.path.exists(MODEL_PATH):
        try:
            checkpoint = torch.load(MODEL_PATH, map_location=device)
            
            # Handle different checkpoint formats
            if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
                state_dict = checkpoint['state_dict']
            else:
                state_dict = checkpoint
            
            # Load with strict=False to handle size mismatches
            model.load_state_dict(state_dict, strict=False)
            logger.info(f"Loaded model checkpoint from {MODEL_PATH}")
            
        except Exception as e:
            logger.warning(f"Failed to load checkpoint: {e}")
            logger.info("Using pretrained model instead")
            
            # Save current model as backup
            torch.save(model.state_dict(), MODEL_PATH.with_suffix(".pt.backup"))
    else:
        logger.info("No existing model found, using pretrained model")
        # Save initial model
        torch.save(model.state_dict(), MODEL_PATH)
        logger.info(f"Saved initial model to {MODEL_PATH}")

    model.eval()
    return model, device, label_dict
