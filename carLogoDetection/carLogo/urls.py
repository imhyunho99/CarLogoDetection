# urls.py
from django.urls import path
from .views import home, search_logo, log, submit_feedback, sentry_debug

urlpatterns = [
    path("", home, name="home"),
    path("search/", search_logo, name="search_logo"),
    path("log/", log, name="log"),
    path("logs/", log, name="logs"),  # Add logs endpoint
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('sentry-debug/', sentry_debug, name='sentry_debug'),
]
