from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import DetectionLog
from .serializers import DetectionLogSerializer
from .utils import searchUtiles
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser


class LogViewSet(viewsets.ModelViewSet):
    queryset = DetectionLog.objects.all()
    serializer_class = DetectionLogSerializer


def home(request):
    print("home render")
    return render(request, "carLogoDetection/home.html")


@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def search_logo(request):
    image = request.FILES.get("image")
    if image:
        predict_label = searchUtiles.search(image)
        DetectionLog.objects.create(logoName=predict_label)
        return Response({"message": f"로고 검색 실행! : {predict_label}"})
    return Response({"error": "이미지 업로드 실패"}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def log(request):
    logs = DetectionLog.objects.all()
    serializer = DetectionLogSerializer(logs, many=True)
    return Response(serializer.data)
