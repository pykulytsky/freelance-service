from django.urls import path
from django.urls import include

from .api.views import LoginAPIView, TestAPI

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('test/', TestAPI.as_view(), name='test')
]
