from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter


from jobs.api.views import *  # noqa

router = DefaultRouter()
router.register('job', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/<int:job_id>/', JobsByUserPerformDetailAPI.as_view(), name="job-by-user"),
    path('favorites-jobs/<int:id>', FavoriteJobsAPI.as_view(), name='favorites-jobs-detail'),
    path('favorites-jobs/', FavoriteJobsListAPI.as_view(), name='favorites-jobs-list'),
    path('proposals/', ProposalListCreateAPI.as_view(), name='proposals-list'),
    path('proposals/<int:id>', ProposalDetailAPI.as_view(), name='proposals-detail')
]
