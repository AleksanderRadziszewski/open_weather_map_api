from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ApiWeatherView.as_view()),
]
