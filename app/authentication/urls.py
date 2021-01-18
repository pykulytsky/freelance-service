from django.urls import path
from django.urls import include

from .api.views import LoginAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login')
]
