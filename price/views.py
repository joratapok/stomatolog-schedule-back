from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from price.models import PriceList, Service
from price.serializers import PriceListSerializer, ServiceSerializer
import re


class PriceListCreateAPIView(generics.ListCreateAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated]


class PriceListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated]


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def split_input_parameter(self):
        chars = re.findall(r'[а-яА-Яa-zA-Z]+', self.request.query_params['service'])
        nums = re.findall(r'\d+', self.request.query_params['service'])
        return chars + nums

    def get_queryset(self):
        queryset = Service.objects.all()
        if 'service' in self.request.query_params:
            filter_queryset = queryset
            for filter_word in self.split_input_parameter():
                filter_queryset = filter_queryset.filter(title__icontains=filter_word)
            return filter_queryset[:10]
        return queryset[:10]


class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
