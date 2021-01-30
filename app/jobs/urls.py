from django.urls import path

from jobs.api.views import JobListAPI, JobDetailAPI, FavoriteJobsAPI, FavoriteJobsListAPI


urlpatterns = [
    path('jobs/', JobListAPI.as_view(), name='job-list'),
    path('jobs/<int:id>/', JobDetailAPI.as_view(), name='job-detail'),
    path('favorites-jobs/<int:id>', FavoriteJobsAPI.as_view(), name='favorites-jobs-detail'),
    path('favorites-jobs/', FavoriteJobsListAPI.as_view(), name='favorites-jobs-list')
]
