from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .api.views import (ActivateUserAPI, DeactivateUserAPI, LoginAPIView,
                        RegisterAPI, TestAPI, UserViewSet)

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('test/', TestAPI.as_view(), name='test'),
    path('activate/<uuid:code>', ActivateUserAPI.as_view(), name='activate'),
    path('deactivate/', DeactivateUserAPI.as_view(), name='deactivate'),
    path('', include(router.urls))
]
