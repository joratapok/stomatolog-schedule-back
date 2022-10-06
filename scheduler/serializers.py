from rest_framework.serializers import ModelSerializer
from .models import Clinic


class ClinicSerializer(ModelSerializer):
    class Meta:
        model = Clinic
        exclude = ['time_zone']
