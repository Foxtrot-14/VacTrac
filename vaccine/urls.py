from django.urls import path
from vaccine.views import *
urlpatterns = [
    path('vaccine/', VaccineAPIView.as_view(),name='vaccine'),
    path('vaccine/<int:pk>/', VaccineDetailAPIView.as_view(), name='getvaccine'),
]