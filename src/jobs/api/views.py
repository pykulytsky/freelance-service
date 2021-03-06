from jobs.creator import JobCreator, ProposalCreator
from jobs.models import *
from jobs.permissions import JobOwnerPermission
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, permission_classes as permission  # noqa
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class JobListAPI(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobListSerializer
    queryset = Job.objects.all()

    def create(self, request):
        data = request.data.copy()

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = {k: data[k] for k in data if k != 'author'}
            JobCreator(
                author=request.user,
                **data
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


class ProposalDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProposalListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Proposal.objects.filter(performer=self.request.user)


class ProposalListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProposalListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Proposal.objects.filter(performer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ProposalCreateSerializer(data=request.data)

        if serializer.is_valid():
            print(f'{serializer.data}')
            ProposalCreator(
                performer=request.user,
                job=Job.objects.get(id=serializer.data['job']),
                **{k: serializer.data[k] for k in serializer.data if k != 'performer' and k != 'job'}
            )()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobsByUserPerformListAPI(APIView):
    permission_classes = (IsAuthenticated)

    def get(self, user_id):
        _user = User.objects.get(user_id)
        jobs = Job.objects.filter(performer=_user)

        serializer = JobListSerializer(jobs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobsByUserPerformDetailAPI(APIView):
    permission_classes = (IsAuthenticated)

    def get(self, user_id, job_id):
        _user = User.objects.get(user_id)
        jobs = Job.objects.filter(performer=_user, id=job_id)

        serializer = JobListSerializer(jobs)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobViewSet(viewsets.ModelViewSet):
    """
    A viewset for manage jobs
    """
    queryset = Job.objects.all()
    serializer_class = JobListSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            data = {k: data[k] for k in data if k != 'author'}

            creator = JobCreator(author=request.user, **data)
            creator()
            if creator.errors:
                return Response(creator.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    @permission(JobOwnerPermission)
    def approve(self, request, pk=None):
        job = self.get_object()
        proposal = job.approve_proposal(request.data['proposal_id'])
        if proposal:
            serializer = ProposalListSerializer(job.approved_proposal)
            return Response(serializer.data, status=status.HTTP_200_OK)
