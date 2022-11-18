from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .models import Clinic, Event, Profile
from .serializers import ClinicSerializer, EventSerializer, UserProfileSerializer


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
        return Clinic.objects.filter(cabinets__cabinet_events__dateStart__startswith=self.get_filter_date(),
                                     cabinets__cabinet_events__doctor=Profile.objects.get(user=self.request.user)
                                     ).distinct()


class EventCreateApiView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user = self.get_object(pk)
        user_serializer = UserProfileSerializer(user, data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        profile = Profile.objects.get(user=user)
        profile.delete()
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
