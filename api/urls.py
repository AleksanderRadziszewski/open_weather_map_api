from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import ApiNumber

from . import views

router = routers.DefaultRouter()
router.register(r"", ApiNumber)

urlpatterns = [
    path('list/', views.ApiNumbersView.as_view()),
    path('', include(router.urls))
]

