import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carLogoDetection.settings")  # 소문자 c 주의
django.setup()


from .train import train
from .trainUtils import replace_model_if_better
from pathlib import Path
import logging

logger = logging.getLogger('deployment')

# Use pathlib for path management
MODEL_DIR = Path(__file__).parent.parent / "models"
RETRAINED_MODEL_PATH = MODEL_DIR / "model_retrained.pt"
CURRENT_MODEL_PATH = MODEL_DIR / "model_current.pt"
FINAL_SAVE_PATH = CURRENT_MODEL_PATH

def retrain_and_replace():
    logger.info("Start retraining...")
    val_dataloader = train()

    if val_dataloader is None:
        logger.info("Training was aborted, skipping replacement.")
        return

    logger.info("Evaluate and decide whether to replace...")
    replaced = replace_model_if_better(
        new_model_path=RETRAINED_MODEL_PATH,
        current_model_path=CURRENT_MODEL_PATH,
        save_path=FINAL_SAVE_PATH,
        val_dataloader=val_dataloader
    )
    if replaced:
        logger.info("Model has been replaced.")
    else:
        logger.info("Model not replaced.")

if __name__ == "__main__":
    retrain_and_replace()
