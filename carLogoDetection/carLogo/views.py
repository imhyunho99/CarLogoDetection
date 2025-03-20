from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import searchUtiles


def home(request):
    print("home render")
    return render(request, "carLogoDetection/home.html")


@csrf_exempt
def search(request):
    """로고 검색 기능"""
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        file_path = default_storage.save(f"search/{image.name}", image)
        print("test learn Post Success")
        predict_label = searchUtiles.search(image)
        return JsonResponse({"message": f"로고 검색 실행! : {predict_label}"})

    return JsonResponse({"error": "이미지 업로드 실패"}, status=400)
