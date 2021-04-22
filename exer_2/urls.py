from django.urls import path
from . import views

urlpatterns = [
    path('steps/', views.ApiWeatherView.as_view()),
]
