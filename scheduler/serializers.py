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
    cabinet_events = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cabinet
        fields = ['id', 'name', 'cabinet_events']

    def get_cabinet_events(self, obj):
        cabinet = obj
        queryset = cabinet.cabinet_events.filter(dateStart__startswith=self.context['filter_date'])
        return EventClinicSerializer(queryset, many=True).data


class ClinicSerializer(ModelSerializer):
    cabinets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Clinic
        fields = ['id', 'title', 'slug', 'cabinets', 'phone', 'is_active']

    def get_cabinets(self, obj):
        clinic = obj
        date = self.context['request'].query_params['date']
        filter_date = f'{date[6:]}-{date[3:5]}-{date[:2]}'
        queryset = clinic.cabinets.filter(cabinet_events__dateStart__startswith=filter_date)
        queryset = CabinetClinicSerializer(queryset, many=True, context={'filter_date': filter_date}).data
        return queryset
