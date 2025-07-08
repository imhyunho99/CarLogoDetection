from django.db import models


class DetectionLog(models.Model):
    logoName = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.logoName

class Feedback(models.Model):
    image = models.ImageField(upload_to='feedback_images/')
    predicted_label = models.CharField(max_length=100)
    correct_label = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_label} → {self.correct_label} ({self.created_at})"


class LogoLabel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

