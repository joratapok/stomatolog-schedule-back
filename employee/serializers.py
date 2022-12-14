from rest_framework import serializers
from django.contrib.auth.models import User
from djoser.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.serializers import ModelSerializer
from djoser.serializers import TokenCreateSerializer
from employee.models import Profile


class ProfileSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_of_birth = serializers.DateField()

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'date_of_birth',
            'phone',
            'image',
            'speciality',
            'clinic'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        if user_data:
            password = user_data.pop('password')
            user = User.objects.create(**user_data)
            if password and user.password != password:
                user.set_password(password)

        clinic = validated_data.pop('clinic')
        profile = Profile.objects.create(user=user, **validated_data)
        profile.clinic.set(clinic)

        user.save()
        profile.save()
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if validated_data['image'] is None:
            validated_data['image'] = instance.image
        instance = super().update(instance, validated_data)

        if user_data:
            password = user_data.pop('password', None)
            for field_name, value in user_data.items():
                setattr(instance.user, field_name, value)
            if password and instance.user.password != password:
                instance.user.set_password(password)
            instance.user.save()
        return instance


class ProfileTokenSerializer(ProfileSerializer):
    token = serializers.CharField(source='user.auth_token.key')

    class Meta:
        model = Profile
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'role',
            'date_of_birth',
            'phone',
            'image',
            'speciality',
            'clinic',
            'token'
        )


class EventProfileSerializer(ProfileSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('password', None)
        return response


class ProfileTokenCreateSerializer(TokenCreateSerializer):
    """
        Переопределение метода validate класса TokenCreateSerializer для
        изменения статус кода с HTTP_400_BAD_REQUEST на HTTP_403_FORBIDDEN
        через class PermissionDenied
    """
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                raise PermissionDenied('permission_denied')
        if self.user and self.user.is_active:
            return attrs
        raise PermissionDenied('permission_denied')
