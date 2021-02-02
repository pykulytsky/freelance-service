from django.urls import path

from jobs.api.views import JobListAPI, JobDetailAPI, FavoriteJobsAPI, FavoriteJobsListAPI, ProposalDetailAPI, ProposalListCreateAPI


urlpatterns = [
    path('jobs/', JobListAPI.as_view(), name='job-list'),
    path('jobs/<int:id>/', JobDetailAPI.as_view(), name='job-detail'),
    path('favorites-jobs/<int:id>', FavoriteJobsAPI.as_view(), name='favorites-jobs-detail'),
    path('favorites-jobs/', FavoriteJobsListAPI.as_view(), name='favorites-jobs-list'),
    path('proposals/', ProposalListCreateAPI.as_view(), name='proposals-list'),
    path('proposals/<int:id>', ProposalDetailAPI.as_view(), name='proposals-detail')
]
