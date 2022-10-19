from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Clinic, Cabinet, Event, Customer, User


class UserClinicSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_name']


class CustomerClinicSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'middle_name']


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['cabinet', 'dateStart', 'dateFinish', 'client', 'doctor']


class EventClinicSerializer(ModelSerializer):
    client = CustomerClinicSerializer(many=False)
    doctor = UserClinicSerializer(many=False)

    class Meta:
        model = Event
        fields = ['id', 'dateStart', 'dateFinish', 'client', 'doctor']


class CabinetSerializer(ModelSerializer):

    class Meta:
        model = Cabinet
        fields = ['clinic', 'name', 'cabinet_events']


class CabinetClinicSerializer(ModelSerializer):
    cabinet_events = EventClinicSerializer(many=True, read_only=True)

    class Meta:
        model = Cabinet
        fields = ['id', 'name', 'cabinet_events']


class ClinicSerializer(ModelSerializer):
    cabinets = CabinetClinicSerializer(many=True)

    class Meta:
        model = Clinic
        fields = ['id', 'title', 'slug', 'cabinets', 'phone', 'is_active']
