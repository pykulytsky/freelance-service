from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import LoginSerializer
from authentication.creator import UserCreateSerializer
from authentication.creator import UserCreateDetailSerializer
from authentication.creator import UserCreator

from rest_framework import generics


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
            new_user = UserCreator(**serializer.data)()

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
    pass


class UserDetailAPI(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserCreateDetailSerializer

    def get(self, request):
        print(f'{request.user=}')

        return Response({'some': 'text'}, status=status.status.HTTP_200_OK)