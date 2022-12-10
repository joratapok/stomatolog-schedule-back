from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from scheduler.models import Clinic, Cabinet, Event, Customer
from django.contrib.auth.models import User
from employee.models import Profile
from employee.serializers import EventUserProfileSerializer, ProfileSerializer

# Неиспользуемые сериализаторы
# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'first_name', 'last_name')
#
#
# class UserClinicSerializer(ModelSerializer):
#     user = UserSerializer(many=False)
#
#     class Meta:
#         model = Profile
#         fields = ('user', )


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


# class CustomerClinicSerializer(ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ('id', 'first_name', 'last_name', 'middle_name')


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventCustomerSerializer(UniqueFieldsMixin,  WritableNestedModelSerializer):
    client = CustomerSerializer()

    class Meta:
        model = Event
        fields = ('cabinet', 'date_start', 'date_finish', 'service', 'status', 'color', 'doctor', 'client')

    def create(self, validated_data):
        client_data = validated_data.pop('client')
        client = Customer.objects.create(**client_data)
        return Event.objects.create(client=client, **validated_data)


class EventClinicSerializer(ModelSerializer):
    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'date_start', 'date_finish', 'service', 'status', 'color', 'client', 'doctor')


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
        queryset = cabinet.cabinet_events.filter(date_start__startswith=self.context['filter_date']).distinct()

        if self.context['profile'].role == 'doctor':
            queryset = queryset.filter(doctor=self.context['profile']).distinct()

        return EventClinicSerializer(queryset, many=True).data


class ClinicSerializer(ModelSerializer):
    cabinets = serializers.SerializerMethodField(read_only=True)
    doctors = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Clinic
        fields = ('id',
                  'title',
                  'slug',
                  'cabinets',
                  'phone',
                  'is_active',
                  'start_of_the_day',
                  'end_of_the_day',
                  'doctors'
                  )

    def get_cabinets(self, obj):
        clinic = obj
        queryset = clinic.cabinets.all()
        if self.context['profile'].role == 'doctor':
            queryset = queryset.filter(cabinet_events__doctor=self.context['profile']).distinct()
        return CabinetClinicSerializer(queryset, many=True, context={'filter_date': self.context['filter_date'],
                                                                     'profile': self.context['profile']}).data

    def get_doctors(self, obj):
        clinic = obj
        queryset = User.objects.filter(profile__clinic=clinic, profile__role='doctor')
        return EventUserProfileSerializer(queryset, many=True).data
