from django.urls import path
from child.views import *
urlpatterns = [
    path('child/', AddChildView.as_view(),name='childadd'),
    path('child/<int:pk>/', ChildDetailAPIView.as_view(), name='getchild'),
]