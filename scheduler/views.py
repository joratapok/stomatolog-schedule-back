from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Clinic
from .serializers import ClinicSerializer

TODAY_DATE = datetime.today().date()


class ClinicListApiView(generics.ListCreateAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if 'date' in self.request.query_params:
            # date format is day-month-year
            date = self.request.query_params['date']
            filter_date = f'{date[6:]}-{date[3:5]}-{date[:2]}'
        else:
            filter_date = TODAY_DATE
        return Clinic.objects.filter(offices__cabinet_events__dateStart__startswith=filter_date)


class ClinicDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Clinic.objects.all()
