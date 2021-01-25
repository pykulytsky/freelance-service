from django.urls import path

from jobs.api.views import JobListAPI, JobDetailAPI


urlpatterns = [
    path('jobs/', JobListAPI.as_view(), name='job-list'),
    path('jobs/<int:id>/', JobDetailAPI.as_view(), name='job-detail')
]
