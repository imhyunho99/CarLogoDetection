import os
from ..train import train
from .trainUtils import replace_model_if_better

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RETRAINED_MODEL_PATH = os.path.join(BASE_DIR, "model_retrained.pt")
CURRENT_MODEL_PATH = os.path.join(BASE_DIR, "utils", "model.pt")  # 현재 모델
FINAL_SAVE_PATH = CURRENT_MODEL_PATH

def retrain_and_replace():
    print("📦 Start retraining...")
    train()  # retrain & save to model_retrained.pt

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
