from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from datetime import datetime

TODAY_DATE = datetime.today()


class EventListApiView(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        filter_date = self.kwargs['date']
        if filter_date:
            queryset = Event.objects.filter(date=filter_date)
        else:
            queryset = Event.objects.filter(date=TODAY_DATE)
        return queryset
