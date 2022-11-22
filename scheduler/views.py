from rest_framework import generics
from datetime import datetime
from employee.models import Profile
from scheduler.models import Clinic, Event
from scheduler.serializers import ClinicSerializer, EventSerializer


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
                'filter_date': self.get_filter_date(),
                'profile': Profile.objects.get(user=self.request.user),
                }

    def get_queryset(self):
        print('AUTH = ', self.request.auth)
        queryset = Clinic.objects.filter(
            cabinets__cabinet_events__dateStart__startswith=self.get_filter_date()).distinct()

        profile = Profile.objects.get(user=self.request.user)

        if profile.role == 'administrator':
            return queryset.filter(id=profile.clinic.first().id).distinct()
        elif profile.role == 'owner':
            return queryset.distinct()
        elif profile.role == 'doctor':
            return queryset.filter(
                cabinets__cabinet_events__doctor=profile).distinct()


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
