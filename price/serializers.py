from rest_framework import serializers
from price.models import PriceList, Service, Teeth, DentalChart


class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class TeethSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teeth
        depth = 1
        fields = '__all__'


class DentalChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalChart
        fields = '__all__'
