from django.urls import path

from jobs.api.views import * # noqa


urlpatterns = [
    path('jobs/', JobListAPI.as_view(), name='job-list'),
    path('jobs/<int:id>/', JobDetailAPI.as_view(), name='job-detail'),
    path('jobs/user/<int:user_id>/', JobsByUserPerformListAPI.as_view(), name="job-by-user"),
    path('user/<int:user_id>/<int:job_id>/', JobsByUserPerformDetailAPI.as_view(), name="job-by-user"),
    path('favorites-jobs/<int:id>', FavoriteJobsAPI.as_view(), name='favorites-jobs-detail'),
    path('favorites-jobs/', FavoriteJobsListAPI.as_view(), name='favorites-jobs-list'),
    path('proposals/', ProposalListCreateAPI.as_view(), name='proposals-list'),
    path('proposals/<int:id>', ProposalDetailAPI.as_view(), name='proposals-detail')
]
