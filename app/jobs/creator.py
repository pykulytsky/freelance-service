from rest_framework import serializers


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
