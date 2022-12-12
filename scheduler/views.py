from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

from employee.models import Profile
from scheduler.models import Clinic, Event, Cabinet, Customer
from scheduler.serializers import ClinicSerializer, EventSerializer, EventCustomerSerializer, CabinetSerializer, \
    CustomerSerializer
from scheduler.permissions import IsAdministrator


TODAY_DATE = datetime.today().date()


class EventListApiView(generics.ListAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

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
        queryset = Clinic.objects.filter(
            cabinets__cabinet_events__date_start__startswith=self.get_filter_date()).distinct()

        if not queryset:
            queryset = Clinic.objects.all()

        profile = Profile.objects.get(user=self.request.user)

        if profile.role == 'administrator':
            return queryset.filter(id=profile.clinic.first().id).distinct()
        elif profile.role == 'owner':
            return queryset.distinct()
        elif profile.role == 'doctor':
            return queryset.filter(cabinets__cabinet_events__doctor=profile).distinct()


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsAdministrator]

    def get_serializer_class(self):
        if isinstance(self.request.data.get('client'), dict):
            return EventCustomerSerializer
        return EventSerializer


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]


class CabinetCreateApiView(generics.CreateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]


class CabinetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]


class CustomerListApiView(generics.ListAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]

    def get_queryset(self):
        if 'last_name' in self.request.query_params:
            return Customer.objects.filter(last_name__istartswith=self.request.query_params['last_name'])[:10]
        return Customer.objects.all()[:10]
