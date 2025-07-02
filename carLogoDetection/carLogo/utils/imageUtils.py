import base64
from io import BytesIO
from PIL import Image


def in_memory_file_to_pil(uploaded_file):
    """InMemoryUploadedFile """
    uploaded_file.seek(0)
    image = Image.open(BytesIO(uploaded_file.read())).convert("RGB")
    return image
