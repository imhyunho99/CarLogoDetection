# urls.py
from django.urls import path
from .views import home, search_logo, log  # log는 로그 확인용 API

urlpatterns = [
    path("", home, name="home"),
    path("search/", search_logo, name="search_logo"),
    path("log/", log, name="log"),  # 로그 확인 API
]
