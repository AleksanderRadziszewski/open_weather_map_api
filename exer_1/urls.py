from django.urls import path
from . import views

urlpatterns = [
    path('growth/', views.ApiTempGrowthView.as_view()),
]
