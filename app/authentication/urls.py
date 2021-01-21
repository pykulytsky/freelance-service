from django.urls import path

from .api.views import LoginAPIView, TestAPI, RegisterAPI, ActivateUserAPI, DeactivateUserAPI, UserDetailAPI

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('test/', TestAPI.as_view(), name='test'),
    path('activate/', ActivateUserAPI.as_view(), name='activate'),
    path('deactivate/', DeactivateUserAPI.as_view(), name='deactivate'),
    path('user/', UserDetailAPI.as_view(), name='user-detail')
]
