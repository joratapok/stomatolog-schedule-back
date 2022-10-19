from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Clinic, Cabinet, Event
from .serializers import ClinicSerializer

TODAY_DATE = datetime.today().date()


class EventListApiView(generics.ListCreateAPIView):
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
