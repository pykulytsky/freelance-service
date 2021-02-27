from rest_framework.permissions import BasePermission
from .models import User


class UserActionPermission(BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs.get('id', None)
        _user = User.objects.get(id=user_id)

        if _user == request.user:
            return True

        raise PermissionError('Wrong authentication credentials provided or you can`t manage this endpoint.')
