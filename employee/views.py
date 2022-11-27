from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


from employee.models import Profile
from employee.serializers import UserProfileSerializer, UserProfileWithoutPasswordSerializer
from employee.permissions import IsOwner

from datetime import datetime, timedelta

import pytz
from rest_framework import exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response



class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        instance = serializer.save()
        print('INSTANCE.PROFILE = ', instance)
        instance.set_password(instance.password)
        instance.save()


class UserUpdateDestroyAPIView(mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]

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


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileWithoutPasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Token.objects.get(key=self.request.auth).user
        except User.DoesNotExist:
            raise Http404


# -----------------------------------------------------------------------------
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


# class ExpiringTokenAuthentication(TokenAuthentication):
#     def authenticate_credentials(self, key):
#         try:
#             token = self.model.objects.get(key=key)
#         except self.model.DoesNotExist:
#             raise exceptions.AuthenticationFailed('Invalid token')
#
#         if not token.user.is_active:
#             raise exceptions.AuthenticationFailed('User inactive or deleted')
#
#         # This is required for the time comparison
#         utc_now = datetime.utcnow()
#         utc_now = utc_now.replace(tzinfo=pytz.utc)
#
#         if token.created < utc_now - timedelta(minutes=5):
#             raise exceptions.AuthenticationFailed('Token has expired')
#
#         return token.user, token
#
#
# class ObtainExpiringAuthToken(ObtainAuthToken):
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
#             print('CREATED ============ ', token.created)
#             print(datetime.now())
#             if not created:
#                 # update the created time of the token to keep it valid
#                 token.created = datetime.utcnow()
#                 token.save()
#
#             return Response({'token': token.key})
#         return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)