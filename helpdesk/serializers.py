from rest_framework import serializers

from .models import *
from personal.serializers import OperatorSerializer, WorkstationSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    operator = OperatorSerializer(required=False, many=True)
    workstation = WorkstationSerializer(required=False, many=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('id', 'updated_at', 'created_at')
