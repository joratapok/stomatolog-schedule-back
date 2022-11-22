from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


from employee.models import Profile
from employee.serializers import UserProfileSerializer


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserUpdateDestroyAPIView(mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               GenericAPIView):
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


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return Token.objects.get(key=self.request.auth).user
        except User.DoesNotExist:
            raise Http404
