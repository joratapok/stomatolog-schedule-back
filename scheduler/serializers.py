from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Clinic, Cabinet, Event, Customer, Profile, User
from rest_framework.response import Response
from rest_framework import status


class UserProfileClinicSerializer(ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    middle_name = serializers.CharField(source='profile.middle_name')
    date_of_birth = serializers.CharField(source='profile.date_of_birth')
    phone = serializers.CharField(source='profile.phone')
    image = serializers.ImageField(source='profile.image')
    speciality = serializers.CharField(source='profile.speciality')
    clinic = serializers.PrimaryKeyRelatedField(queryset=Clinic.objects.all(), many=True)

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'first_name',
                  'last_name',
                  'middle_name',
                  'date_of_birth',
                  'phone',
                  'image',
                  'speciality',
                  'clinic',
                  ]

    def create(self, validated_data):
        print('VALID = ', validated_data['profile']['middle_name'])
        user = User.objects.create(username=validated_data['username'],
                                   password=validated_data['password'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'])

        profile = Profile.objects.create(user=user,
                                         middle_name=validated_data['profile']['middle_name'],
                                         date_of_birth=validated_data['profile']['date_of_birth'],
                                         phone=validated_data['profile']['phone'],
                                         image=validated_data['profile']['image'],
                                         speciality=validated_data['profile']['speciality'],
                                         )

        for clinic in validated_data['clinic']:
            profile.clinic.add(clinic.id)

        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class UserClinicSerializer(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['user']


class CustomerClinicSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'middle_name']


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
        queryset = clinic.cabinets.filter(cabinet_events__dateStart__startswith=self.context['filter_date'])
        return CabinetClinicSerializer(queryset, many=True, context={'filter_date': self.context['filter_date']}).data
