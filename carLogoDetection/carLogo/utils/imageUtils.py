import base64
from io import BytesIO
from PIL import Image


def in_memory_file_to_pil(uploaded_file):
    """InMemoryUploadedFile 객체를 PIL 이미지로 변환"""
    # 파일 포인터를 처음으로 이동
    uploaded_file.seek(0)

    # 파일 데이터를 읽어서 BytesIO로 변환 후, PIL로 열기
    image = Image.open(BytesIO(uploaded_file.read())).convert("RGB")

    return image
