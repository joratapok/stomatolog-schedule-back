from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from price.models import Teeth, DentalChart
from price.serializers import TeethListSerializer, TeethCreateSerializer, DentalChartCustomerSerializer
from scheduler.models import Clinic, Cabinet, Event, Customer, DutyShift
from employee.serializers import EventProfileSerializer


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CustomerDetailSerializer(ModelSerializer):
    dental_chart = DentalChartCustomerSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    services = TeethCreateSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        teeth_data = validated_data.pop('services')
        new_event = Event.objects.create(**validated_data)

        for tooth in teeth_data:
            dental_services = tooth.pop('dental_services')
            new_tooth = Teeth.objects.create(event=new_event, dental_chart=new_event.client.dental_chart, **tooth)
            new_tooth.dental_services.set(dental_services)
            new_tooth.save()

        return new_event

    def update(self, instance, validated_data):
        teeth_data = validated_data.pop('services')
        instance = super().update(instance, validated_data)

        if teeth_data:
            for tooth in teeth_data:
                dental_services = tooth.pop('dental_services')

                tooth_obj = Teeth.objects.filter(event=instance)
                tooth_obj.update(**tooth)
                tooth_obj[0].dental_services.set(dental_services)

        return instance


class EventCustomerSerializer(UniqueFieldsMixin,  WritableNestedModelSerializer):
    client = CustomerSerializer()
    services = TeethCreateSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        teeth_data = validated_data.pop('services')
        client_data = validated_data.pop('client')

        client = Customer.objects.create(**client_data)
        new_event = Event.objects.create(client=client, **validated_data)

        for tooth in teeth_data:
            dental_services = tooth.pop('dental_services')
            new_tooth = Teeth.objects.create(event=new_event, dental_chart=new_event.client.dental_chart, **tooth)
            new_tooth.dental_services.set(dental_services)
            new_tooth.save()

        return new_event


class EventClinicSerializer(ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    services = serializers.SerializerMethodField()

    class Meta:
        model = Event
        depth = 1
        fields = ('id', 'date_start', 'date_finish', 'services', 'status', 'color', 'comment', 'client', 'doctor')

    def get_services(self, event):
        queryset = event.services.all()
        return TeethListSerializer(queryset, many=True).data


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ('clinic', 'name')


class DutyShiftSerializer(ModelSerializer):
    class Meta:
        model = DutyShift
        fields = '__all__'


class CabinetClinicSerializer(ModelSerializer):
    cabinet_events = serializers.SerializerMethodField(read_only=True)
    duty_shift = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cabinet
        fields = ('id', 'name', 'cabinet_events', 'duty_shift')

    def get_cabinet_events(self, obj):
        cabinet = obj
        queryset = cabinet.cabinet_events.filter(date_start__startswith=self.context['filter_date']).distinct()

        if self.context['profile'].role == 'doctor':
            queryset = queryset.filter(doctor=self.context['profile']).distinct()

        return EventClinicSerializer(queryset, many=True).data

    def get_duty_shift(self, obj):
        cabinet = obj
        queryset = cabinet.duty_shift_cabinet.filter(date_start__startswith=self.context['filter_date'])
        return DutyShiftSerializer(queryset, many=True).data


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
                  'is_main',
                  'start_of_the_day',
                  'end_of_the_day',
                  'doctors',
                  'price_list'
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
        queryset = clinic.profiles.filter(role='doctor')
        return EventProfileSerializer(queryset, many=True).data
