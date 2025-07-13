import os
import subprocess
from pathlib import Path
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carLogoDetection.settings")
django.setup()

FEEDBACK_DIR = Path(__file__).resolve().parent.parent / "media" / "feedback_images"
THRESHOLD = 50
TRAIN_SCRIPT = Path(__file__).resolve().parent / "train.py"

def count_feedback_images():
    return len([f for f in FEEDBACK_DIR.iterdir() if f.is_file()])

def delete_feedback_images():
    for f in FEEDBACK_DIR.iterdir():
        if f.is_file():
            f.unlink()

def main():
    if count_feedback_images() >= THRESHOLD:
        print("[INFO] Images over 50")
        result = subprocess.run(
            ["python", str(TRAIN_SCRIPT)],
            capture_output=True,
            text=True
        )
        print("[TRAIN OUTPUT]:\n", result.stdout)
        if result.returncode == 0:
            print("[INFO] retrain_success")
            delete_feedback_images()
        else:
            print("[ERROR] retrain_fail", result.stderr)

if __name__ == "__main__":
    main()
