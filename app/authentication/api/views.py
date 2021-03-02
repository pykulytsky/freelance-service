from authentication.tasks import send_new_password
from authentication.utils import generate_random_password, get_client_ip
from authentication.permissions import UserActionPermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer, PasswordResetSerializer, UserPublicSerializer, PasswordSerializer
from authentication.creator import UserCreateSerializer
from authentication.creator import UserCreator

from authentication.models import User
from rest_framework import viewsets
from rest_framework.decorators import action


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'data': 'success'
        },
        status=status.HTTP_200_OK)


class RegisterAPI(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                new_user = UserCreator(**serializer.data)()
            except TypeError as e:
                return Response({
                    'error': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {'token': new_user.token},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class ActivateUserAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, code):
        if request.user.is_active is False:
            if request.user.email_verification_code == code:
                request.user.is_active = True
                request.user.email_verified = True
                request.user.save()
            return Response({'info': 'activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'info': 'user already activated'}, status=status.HTTP_400_BAD_REQUEST)


class DeactivateUserAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if request.user.is_active is True:
            request.user.is_active = False
            request.user.save()
            return Response({'info': 'deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'info': 'user already deactivated'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserPublicSerializer
    permission_classes = (IsAuthenticated, UserActionPermission)

    @action(detail=True, methods=['POST'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True)
    def reset_password(self, request, pk=None):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = generate_random_password()
            request.user.set_password(new_password)
            request.user.save()

            ip = get_client_ip(request)
            send_new_password.delay(request.user.id, new_password, ip)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No user with that email address'
            }, status=status.HTTP_400_BAD_REQUEST)
