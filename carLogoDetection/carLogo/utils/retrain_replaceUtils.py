import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carLogoDetection.settings")  # 소문자 c 주의
django.setup()


from .train import train
from .trainUtils import replace_model_if_better

RETRAINED_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/model_retrained.pt")
CURRENT_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../models/model_current.pt")
FINAL_SAVE_PATH = CURRENT_MODEL_PATH

def retrain_and_replace():
    print("Start retraining...")
    train()

    print("Evaluate and decide whether to replace...")
    replaced = replace_model_if_better(
        new_model_path=RETRAINED_MODEL_PATH,
        current_model_path=CURRENT_MODEL_PATH,
        save_path=FINAL_SAVE_PATH,
    )
    if replaced:
        print("Model has been replaced.")
    else:
        print("Model not replaced.")

if __name__ == "__main__":
    retrain_and_replace()
