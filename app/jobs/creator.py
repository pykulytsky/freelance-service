from django.db.models import fields
from .models import Job

from rest_framework import serializers

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'