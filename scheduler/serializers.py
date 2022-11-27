from django.db.models import Prefetch
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from scheduler.models import Clinic, Cabinet, Event, Customer
from django.contrib.auth.models import User
from employee.models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class UserClinicSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ('user', )


class CustomerClinicSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'middle_name')


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventClinicSerializer(ModelSerializer):
    client = CustomerClinicSerializer(many=False)
    doctor = UserClinicSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'dateStart', 'dateFinish', 'service', 'status', 'color', 'client', 'doctor')


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ('clinic', 'name')


class CabinetClinicSerializer(ModelSerializer):
    cabinet_events = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cabinet
        fields = ('id', 'name', 'cabinet_events')

    def get_cabinet_events(self, obj):
        cabinet = obj
        queryset = cabinet.cabinet_events.filter(dateStart__startswith=self.context['filter_date']).distinct()
        # queryset = cabinet.objects.all().prefetch_related(
        #     Prefetch(
        #         'cabinet_events',
        #         queryset=Event.objects.filter(dateStart__startswith=self.context['filter_date'])
        #     )
        # )
        if self.context['profile'].role == 'doctor':
            queryset = queryset.filter(doctor=self.context['profile']).distinct()
        return EventClinicSerializer(queryset, many=True).data


class ClinicSerializer(ModelSerializer):
    cabinets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Clinic
        fields = ('id', 'title', 'slug', 'cabinets', 'phone', 'is_active')

    def get_cabinets(self, obj):
        clinic = obj
        # queryset = clinic.cabinets.filter(cabinet_events__dateStart__startswith=self.context['filter_date']).distinct()
        # Мои вставки кода
        queryset = clinic.cabinets.all()
        # ---------------------------

        if self.context['profile'].role == 'doctor':
            queryset = queryset.filter(cabinet_events__doctor=self.context['profile']).distinct()
        return CabinetClinicSerializer(queryset, many=True, context={'filter_date': self.context['filter_date'],
                                                                     'profile': self.context['profile']}).data
