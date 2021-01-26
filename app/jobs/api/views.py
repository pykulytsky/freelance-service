from rest_framework.response import Response
from jobs.models import *
from .serializers import *

from jobs.creator import JobCreateSerializer, JobCreator

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from jobs.permissions import JobOwnerPermission

from datetime import date, datetime


class JobListAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobListSerializer
    queryset = Job.objects.all()

    def create(self, request):
        data = request.data.copy()
        data.update({
            'author': request.user
        })

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            JobCreator(
                author=request.user,
                **serializer.data
            )()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, JobOwnerPermission]
    lookup_field = 'id'
    queryset = Job.objects.all()
    serializer_class = JobDetailSerializer
