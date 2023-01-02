from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import TrigramSimilarity
from price.models import PriceList, Service
from price.serializers import PriceListSerializer, ServiceSerializer
from scheduler.permissions import IsOwnerOrAdministrator


class PriceListCreateAPIView(generics.ListCreateAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class PriceListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PriceList.objects.all()
    serializer_class = PriceListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class ServiceListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]

    # def get_queryset(self):
    #     if 'service' in self.request.query_params:
    #         return Service.objects.filter(title__icontains=self.request.query_params['service'])[:10]
    #     return Service.objects.all()[:10]

    def get_queryset(self):
        if 'service' in self.request.query_params:
            return Service.objects.annotate(
                similarity=TrigramSimilarity('title', self.request.query_params['service']),
                ).filter(similarity__gt=0.1)[:10]
        return Service.objects.all()[:10]


class ServiceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]