from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from rest_framework.response import Response

from employee.models import Profile
from scheduler.models import Clinic, Event, Cabinet, Customer
from scheduler.serializers import ClinicSerializer, EventSerializer, CabinetSerializer, EventCustomerSerializer
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
    # serializer_class = EventSerializer
    # serializer_class = EventCustomerSerializer
    permission_classes = [IsAdministrator]

    def get_serializer_class(self):
        if self.request.data.get('client'):
            self.serializer_class = EventCustomerSerializer
        else:
            self.serializer_class = EventSerializer
        return self.serializer_class

    # def post(self, request, *args, **kwargs):
    #     if request.data.get('client_first_name'):
    #         new_client = Customer.objects.create(
    #             first_name=request.data['client_first_name'],
    #             last_name=request.data['client_last_name'],
    #             middle_name=request.data['client_middle_name'],
    #             date_of_birth=request.data['client_date_of_birth'],
    #             gender=request.data['client_gender'],
    #             phone=request.data['client_phone'],
    #         )
    #         new_event = Event.objects.create(
    #             cabinet=Cabinet.objects.get(pk=request.data['cabinet']),
    #             date_start=request.data['date_start'],
    #             date_finish=request.data['date_finish'],
    #             service=request.data['service'],
    #             status=request.data['status'],
    #             color=request.data['color'],
    #             client=new_client,
    #             doctor=Profile.objects.get(pk=request.data['doctor']),
    #         )
    #         return Response(EventSerializer(new_event).data, status=status.HTTP_201_CREATED)
    #     return self.create(request, *args, **kwargs)


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdministrator]


class CabinetCreateApiView(generics.CreateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAdministrator]


class CabinetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAdministrator]
