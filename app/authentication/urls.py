from django.urls import path
from django.urls import include

from .api.views import LoginAPIView, TestAPI, RegisterAPI

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('test/', TestAPI.as_view(), name='test')
]
