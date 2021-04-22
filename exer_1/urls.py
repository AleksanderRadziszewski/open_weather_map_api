from django.urls import path
from . import views

urlpatterns = [
    path('growth/', views.ApiWeatherView.as_view()),
]
