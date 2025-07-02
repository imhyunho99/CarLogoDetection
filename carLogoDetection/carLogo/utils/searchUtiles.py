import torch
from torchvision import transforms
from . import imageUtils

# transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


def search(image, model, device, label_dict):
    image = imageUtils.in_memory_file_to_pil(image)
    input_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        output = output.softmax(dim=1)
        predicted_label = label_dict[output.argmax(dim=1).item()]

    return predicted_label
