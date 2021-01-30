from datetime import datetime
import jwt

from django.conf import settings
from rest_framework import authentication, exceptions
from authentication.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    _AUTHENTICATION_HEADER_PREFIX = 'Bearer'

    def authenticate(self, request) -> tuple:
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self._AUTHENTICATION_HEADER_PREFIX.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)

        except:
            message = 'Can`t authenticate, token didn`t match'
            raise exceptions.AuthenticationFailed(message)

        if payload.get(
            'exp',
            datetime.now().timestamp()
        ) < datetime.now().timestamp():
            raise exceptions.AuthenticationFailed("JWT token expired, please relogin to get new token")

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            if not user.is_activate:

                if 'activate' not in request._request.environ.get("PATH_INFO", '').split('/'):
                    message = 'Inactive user'
                    raise exceptions.AuthenticationFailed(message)

                if 'deactivate' not in request._request.environ.get("PATH_INFO", '').split('/'):
                    message = 'Inactive user'
                    raise exceptions.AuthenticationFailed(message)

        except AttributeError:
            if not user.is_active and 'activate' not in str(request):
                message = 'Inactive user'
                raise exceptions.AuthenticationFailed(message)

        return (user, token)
