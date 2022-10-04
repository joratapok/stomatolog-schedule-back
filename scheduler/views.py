from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Event, Clinic, Cabinet
from .serializers import EventSerializer


TODAY_DATE = datetime.today().date()


class ClinicApiView(APIView):
    pass


class EventListApiView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        filter_date = ''
        if 'date' in self.request.query_params:
            # date format is day-month-year
            date = self.request.query_params['date']
            filter_date = f'{date[6:]}-{date[3:5]}-{date[:2]}'
        else:
            filter_date = TODAY_DATE
        return Clinic.objects.filter()
        # return Event.objects.filter(dateStart__startswith=filter_date)


class EventDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all()  # filter(cabinet__clinic__slug=self.kwargs['clinic'])
