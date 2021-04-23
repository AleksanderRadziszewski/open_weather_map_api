from django.urls import path
from . import views

urlpatterns = [
    path('steps/', views.ApiTempStepView.as_view()),
]
