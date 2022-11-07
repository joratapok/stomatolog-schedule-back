from django.db.models import Subquery
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Clinic, Cabinet, Event
from .serializers import ClinicSerializer, CabinetClinicSerializer, CabinetSerializer, EventSerializer
from django.db.models import Subquery

TODAY_DATE = datetime.today().date()


class ClinicListApiView(generics.ListAPIView):
    serializer_class = ClinicSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'date' in self.request.query_params:
            # date format is day-month-year
            date = self.request.query_params['date']
            filter_date = f'{date[6:]}-{date[3:5]}-{date[:2]}'
        else:
            filter_date = TODAY_DATE
        return Clinic.objects.filter(cabinets__cabinet_events__dateStart__startswith=filter_date)


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
