from rest_framework.response import Response
from rest_framework.views import APIView
from jobs.models import *
from .serializers import *

from jobs.creator import JobCreator

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from jobs.permissions import JobOwnerPermission


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


class FavoriteJobsAPI(APIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    serializer_class = JobDetailSerializer

    def get_queryset(self):
        return FavoritesJobs.objects.get(user=self.request.user).jobs.all()

    def post(self, request, id):
        user = request.user
        job = Job.objects.get(id=id)

        favorites_list = FavoritesJobs.objects.get(user=user)
        favorites_list.jobs.add(job)

        serializer = self.serializer_class(job)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class FavoriteJobsListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jobs = FavoritesJobs.objects.get(user=user).jobs.all()
        serializer = JobListSerializer(jobs, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
