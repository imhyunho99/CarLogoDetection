from django.urls import path
from .views import home, search

urlpatterns = [
    path("", home, name="home"),  # http://127.0.0.1:8000/ 에 접속하면 home 뷰 실행
    path("search/", search, name="search"),
]
