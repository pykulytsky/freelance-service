from rest_framework.permissions import BasePermission

from .models import Job


class JobOwnerPermission(BasePermission):
    """
    Check if current user is owner of referensed job.
    """

    def has_permission(self, request, view):
        job_id = view.kwargs.get('id', None) or view.kwargs.get('pk', None)
        _job = Job.objects.get(id=job_id)

        if _job.author == request.user:
            return True

        raise PermissionError("You have no permissions to manage this job")
