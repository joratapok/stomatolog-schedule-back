from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from employee.models import Profile
from price.models import Teeth
from price.serializers import TeethListSerializer, TeethCreateSerializer, DentalChartCustomerSerializer
from scheduler.models import Clinic, Cabinet, Event, Customer, DutyShift, TreatmentPlan
from employee.serializers import EventProfileSerializer


class TreatmentPlanSerializer(ModelSerializer):
    class Meta:
        model = TreatmentPlan
        fields = ('tooth', 'plan')


class OnlyClinicSerializer(ModelSerializer):

    class Meta:
        model = Clinic
        exclude = ('time_zone', )


class CustomerSerializer(ModelSerializer):
    date_of_birth = serializers.DateField()
    treatment_plan = TreatmentPlanSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        treatment_plan_data = validated_data.pop('treatment_plan') if 'treatment_plan' in validated_data else None
        customer = Customer.objects.create(**validated_data)

        if treatment_plan_data is not None:
            for treatment_plan in treatment_plan_data:
                TreatmentPlan.objects.create(customer=customer, **treatment_plan)
        return customer

    def update(self, instance, validated_data):
        treatment_plan_data = validated_data.pop('treatment_plan') if 'treatment_plan' in validated_data else None
        if treatment_plan_data is not None:
            TreatmentPlan.objects.filter(customer=instance).delete()

            for treatment_plan in treatment_plan_data:
                TreatmentPlan.objects.create(customer=instance, **treatment_plan)
        instance = super().update(instance, validated_data)
        return instance


class CustomerDetailSerializer(ModelSerializer):
    dental_chart = DentalChartCustomerSerializer()
    treatment_plan = TreatmentPlanSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    services = TeethCreateSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        teeth_data = validated_data.pop('services') if 'services' in validated_data else None
        new_event = Event.objects.create(**validated_data)

        if teeth_data:
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
            Teeth.objects.filter(event=instance).delete()

            for tooth in teeth_data:
                dental_services = tooth.pop('dental_services')
                new_tooth = Teeth.objects.create(event=instance, dental_chart=instance.client.dental_chart, **tooth)
                new_tooth.dental_services.set(dental_services)

        return instance


class EventCustomerSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    client = CustomerSerializer()
    services = TeethCreateSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        teeth_data = validated_data.pop('services') if 'services' in validated_data else None
        client_data = validated_data.pop('client')

        client = Customer.objects.create(**client_data)
        new_event = Event.objects.create(client=client, **validated_data)

        if teeth_data:
            for tooth in teeth_data:
                dental_services = tooth.pop('dental_services')
                new_tooth = Teeth.objects.create(event=new_event, dental_chart=new_event.client.dental_chart, **tooth)
                new_tooth.dental_services.set(dental_services)
                new_tooth.save()

        return new_event


class EventClinicSerializer(ModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    services = TeethListSerializer(many=True)

    class Meta:
        model = Event
        depth = 1
        fields = (
            'id', 'date_start', 'date_finish', 'services', 'status', 'color', 'comment', 'client', 'doctor', 'invoice'
        )


class CabinetSerializer(ModelSerializer):
    class Meta:
        model = Cabinet
        fields = ('clinic', 'name', 'is_active')


class DutyShiftSerializer(ModelSerializer):
    class Meta:
        model = DutyShift
        fields = '__all__'


class CabinetClinicSerializer(ModelSerializer):
    cabinet_events = serializers.SerializerMethodField(read_only=True)
    duty_shift = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cabinet
        fields = ('id', 'name', 'is_active', 'cabinet_events', 'duty_shift')

    def get_cabinet_events(self, obj):
        cabinet = obj
        queryset = cabinet.cabinet_events.filter(date_start__startswith=self.context['filter_date']).distinct()
        return EventClinicSerializer(queryset, many=True).data

    def get_duty_shift(self, obj):
        cabinet = obj
        queryset = cabinet.duty_shift_cabinet.filter(date_start__startswith=self.context['filter_date'])
        return DutyShiftSerializer(queryset, many=True).data


class ClinicSerializer(ModelSerializer):
    cabinets = serializers.SerializerMethodField(read_only=True)
    doctors = serializers.SerializerMethodField(read_only=True)
    administrators = serializers.SerializerMethodField(read_only=True)

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
                  'administrators',
                  'price_list'
                  )

    def get_cabinets(self, obj):
        clinic = obj
        queryset = clinic.cabinets.all()
        return CabinetClinicSerializer(
            queryset, many=True, context={'filter_date': self.context['filter_date']}).data

    @staticmethod
    def get_doctors(clinic):
        queryset = Profile.objects.all().select_related('user').prefetch_related('clinic').filter(
            role='doctor',
            clinic=clinic
        )
        return EventProfileSerializer(queryset, many=True).data

    @staticmethod
    def get_administrators(clinic):
        queryset = Profile.objects.all().select_related('user').prefetch_related('clinic').filter(
            role='administrator',
            clinic=clinic
        )
        return EventProfileSerializer(queryset, many=True).data
