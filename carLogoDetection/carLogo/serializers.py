from rest_framework import serializers
from .models import DetectionLog


class DetectionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionLog
        fields = "__all__"
