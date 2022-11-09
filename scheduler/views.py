from django.db.models import Subquery
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Clinic, Event
from .serializers import ClinicSerializer, EventSerializer
from django.db.models import Subquery

TODAY_DATE = datetime.today().date()


class ClinicListApiView(generics.ListAPIView):
    serializer_class = ClinicSerializer
    # permission_classes = [IsAuthenticated]

    def get_filter_date(self):
        if 'date' in self.request.query_params:
            # date format is day-month-year
            date = self.request.query_params['date']
            return f'{date[6:]}-{date[3:5]}-{date[:2]}'
        else:
            return TODAY_DATE

    def get_serializer_context(self):
        return {'request': self.request,
                'filter_date': self.get_filter_date()
                }

    def get_queryset(self):
        return Clinic.objects.filter(cabinets__cabinet_events__dateStart__startswith=self.get_filter_date())


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
