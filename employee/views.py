from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from djoser.views import TokenCreateView, TokenDestroyView

from employee.models import Profile
from employee.serializers import ProfileTokenCreateSerializer, ProfileSerializer, ProfileTokenSerializer
from employee.permissions import IsOwner
from scheduler.permissions import IsOwnerOrAdministrator


class ProfileCreateApiView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]


class ProfileRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all().select_related('user').prefetch_related('clinic')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdministrator]

    def delete(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        user = User.objects.get(profile=profile)
        profile.delete()
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Profile.objects.select_related('user').get(user=self.request.user)
        except Profile.DoesNotExist:
            raise Http404


class ProfileTokenCreateView(TokenCreateView):
    """
        Переопределение сериализатора класса TokenCreateView
    """
    serializer_class = ProfileTokenCreateSerializer


class ProfileTokenDestroyView(TokenDestroyView):
    """
        Переопределение urls класса TokenDestroyView
    """
    pass
