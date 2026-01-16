# carLogo/views.py
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import DetectionLog, Feedback, LogoLabel
from .serializers import DetectionLogSerializer
from .utils.searchUtiles import search
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import time
import logging

logger = logging.getLogger(__name__)

# Global model cache
model = None
device = None
label_dict = None

def load_model_if_needed():
    """Load model only when needed (lazy loading)"""
    global model, device, label_dict
    if model is None:
        from .utils.model_loader import load_model
        model, device, label_dict = load_model()
        logger.info("Model loaded successfully")
    return model, device, label_dict

class LogViewSet(viewsets.ModelViewSet):
    queryset = DetectionLog.objects.all()
    serializer_class = DetectionLogSerializer

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    return render(request, "carLogoDetection/home.html")

@csrf_exempt
@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([AllowAny])
def search_logo(request):
    start_time = time.time()
    
    image = request.FILES.get("image")
    if not image:
        return Response({"error": "No image provided"}, status=400)
    
    try:
        # Load model lazily
        model, device, label_dict = load_model_if_needed()
        
        # Perform prediction
        predict_label = search(image, model, device, label_dict)
        
        # Log the detection
        DetectionLog.objects.create(logoName=predict_label)
        
        # Log performance
        duration = time.time() - start_time
        logger.info(f"Logo detection completed in {duration:.3f}s - Result: {predict_label}")
        
        return Response({
            "predicted_label": predict_label,
            "processing_time": f"{duration:.3f}s"
        })
        
    except Exception as e:
        logger.error(f"Logo detection failed: {str(e)}")
        return Response({"error": "Detection failed"}, status=500)

@api_view(["GET"])
@permission_classes([AllowAny])
def log(request):
    # Cache logs for 5 minutes
    cache_key = "detection_logs"
    cached_logs = cache.get(cache_key)
    
    if cached_logs is None:
        logs = DetectionLog.objects.all().order_by('-date')[:100]  # Limit to 100 recent logs
        serializer = DetectionLogSerializer(logs, many=True)
        cached_logs = serializer.data
        cache.set(cache_key, cached_logs, 300)  # Cache for 5 minutes
    
    return Response(cached_logs)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@permission_classes([AllowAny])
def submit_feedback(request):
    image = request.FILES.get('image')
    predicted_label = request.data.get('predicted_label')
    correct_label = request.data.get('correct_label')

    if not all([image, predicted_label, correct_label]):
        return Response({"error": "image, predicted_label, correct_label are required."},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        logo_label, created = LogoLabel.objects.get_or_create(name=correct_label.strip())

        feedback = Feedback.objects.create(
            image=image,
            predicted_label=predicted_label,
            correct_label=logo_label.name
        )
        
        # Clear logs cache when new feedback is added
        cache.delete("detection_logs")
        
        logger.info(f"Feedback submitted: {predicted_label} -> {correct_label}")
        
        return Response({"message": "Feedback submitted", "id": feedback.id}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        logger.error(f"Feedback submission failed: {str(e)}")
        return Response({"error": "Feedback submission failed"}, status=500)

def sentry_debug(request):
    division_by_zero = 1 / 0
    return Response({"error": "This should not be reached"}, status=500)
