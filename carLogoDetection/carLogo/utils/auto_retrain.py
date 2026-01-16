import os
from pathlib import Path
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carLogoDetection.settings")
django.setup()

from .retrain_replaceUtils import retrain_and_replace

FEEDBACK_DIR = Path(__file__).resolve().parent.parent / "media" / "feedback_images"
THRESHOLD = 50

def count_feedback_images():
    return len([f for f in FEEDBACK_DIR.iterdir() if f.is_file()])

def delete_feedback_images():
    for f in FEEDBACK_DIR.iterdir():
        if f.is_file():
            f.unlink()

def main():
    if count_feedback_images() >= THRESHOLD:
        print("[INFO] Images over 50, starting retraining and replacement process.")
        try:
            retrain_and_replace()
            print("[INFO] Retraining and replacement process finished.")
            # decide whether to delete images after the process
            # delete_feedback_images()
        except Exception as e:
            print(f"[ERROR] An error occurred during the retraining and replacement process: {e}")

if __name__ == "__main__":
    main()
