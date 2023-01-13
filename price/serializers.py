from rest_framework import serializers
from price.models import PriceList, Service, DentalChart, Teeth


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class DentalChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalChart
        fields = '__all__'


class TeethListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teeth
        depth = 1
        fields = ('tooth_number', 'dental_services')


class TeethCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teeth
        fields = ('tooth_number', 'dental_services')


class TeethListCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teeth
        depth = 1
        fields = ('tooth_number', 'dental_services', 'event')


class DentalChartCustomerSerializer(serializers.ModelSerializer):
    teeth = TeethListCustomerSerializer(many=True)

    class Meta:
        model = DentalChart
        fields = ('id', 'teeth')
