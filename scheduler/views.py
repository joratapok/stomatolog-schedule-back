from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from scheduler.models import Clinic, Event, Cabinet, Customer, DutyShift
from scheduler.serializers import ClinicSerializer, EventSerializer, EventCustomerSerializer, CabinetSerializer, \
    CustomerSerializer, CustomerDetailSerializer, DutyShiftSerializer
from scheduler.permissions import IsOwnerOrAdministrator
from scheduler.utils import render_pdf_view

TODAY_DATE = datetime.today().date()


class ClinicListApiView(generics.ListAPIView):
    queryset = Clinic.objects.all().prefetch_related('cabinets')
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

    def get_filter_date(self):
        if 'date' in self.request.query_params:
            # date format from url is day-month-year
            date = self.request.query_params['date']
            return f'{date[6:]}-{date[3:5]}-{date[:2]}'
        else:
            return TODAY_DATE

    def get_serializer_context(self):
        return {
            'request': self.request,
            'filter_date': self.get_filter_date(),
            'profile': self.request.user.profile,
        }


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]

    def get_serializer_class(self):
        if isinstance(self.request.data.get('client'), dict):
            return EventCustomerSerializer
        return EventSerializer


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all().prefetch_related('services__dental_services__teeth')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class CabinetCreateApiView(generics.CreateAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class CabinetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class CustomerListCreateApiView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]

    def get_queryset(self):
        if 'lastName' in self.request.query_params:
            return Customer.objects.filter(last_name__istartswith=self.request.query_params['lastName'])[:10]
        return Customer.objects.all()[:10]


class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class CustomerDetailRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class DutyShiftListCreateApiView(generics.ListCreateAPIView):
    queryset = DutyShift.objects.all()
    serializer_class = DutyShiftSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class DutyShiftRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DutyShift.objects.all()
    serializer_class = DutyShiftSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


@api_view(['GET'])
def get_invoice_of_payment(request, pk):
    event = Event.objects.get(pk=pk)
    total_sum = 0
    for service in event.services.all():
        for dent_serv in service.dental_services.all():
            total_sum += dent_serv.price * service.count
    context = {
        'event': event,
        'clinic': event.doctor.clinic.all()[0].title,
        'services': event.services.all(),
        'total_sum': total_sum,
        'total_sum_with_discount': int(total_sum) * (1.0 - event.client.discount / 100.0)
    }
    pdf_template = 'scheduler/pdf.html'
    return render_pdf_view(pdf_template, context, event)
