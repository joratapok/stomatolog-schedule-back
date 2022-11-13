from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Clinic, Cabinet, Event, Customer, Profile, User
from rest_framework.response import Response
from rest_framework import status
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin


class ProfileSerializer(UniqueFieldsMixin,  WritableNestedModelSerializer):
    class Meta:
        model = Profile
        fields = ('middle_name', 'date_of_birth', 'phone', 'image', 'speciality', 'clinic')


class UserProfileSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'profile')


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
        fields = ('cabinet', 'dateStart', 'dateFinish', 'client', 'doctor')


class EventClinicSerializer(ModelSerializer):
    client = CustomerClinicSerializer(many=False)
    doctor = UserClinicSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'dateStart', 'dateFinish', 'client', 'doctor')


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ('clinic', 'name', 'cabinet_events')


class CabinetClinicSerializer(ModelSerializer):
    cabinet_events = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cabinet
        fields = ('id', 'name', 'cabinet_events')

    def get_cabinet_events(self, obj):
        cabinet = obj
        queryset = cabinet.cabinet_events.filter(dateStart__startswith=self.context['filter_date'],
                                                 doctor=self.context['profile']
                                                 )
        return EventClinicSerializer(queryset, many=True).data


class ClinicSerializer(ModelSerializer):
    cabinets = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Clinic
        fields = ('id', 'title', 'slug', 'cabinets', 'phone', 'is_active')

    def get_cabinets(self, obj):
        clinic = obj
        queryset = clinic.cabinets.filter(cabinet_events__dateStart__startswith=self.context['filter_date'],
                                          cabinet_events__doctor=self.context['profile']
                                          )
        return CabinetClinicSerializer(queryset, many=True, context={'filter_date': self.context['filter_date'],
                                                                     'profile': self.context['profile']}).data
