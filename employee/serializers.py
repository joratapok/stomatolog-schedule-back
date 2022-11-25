from rest_framework import serializers
from employee.models import Profile
from django.contrib.auth.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin
from djoser.serializers import TokenCreateSerializer
from djoser.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from djoser.serializers import TokenSerializer


class ProfileSerializer(UniqueFieldsMixin,  WritableNestedModelSerializer):
    date_of_birth = serializers.DateField()

    class Meta:
        model = Profile
        fields = ('middle_name', 'role', 'date_of_birth', 'phone', 'image', 'speciality', 'clinic')


class UserProfileSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'profile')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        profile = instance.profile
        profile_data = validated_data.pop('profile')

        profile.middle_name = profile_data['middle_name']
        profile.role = profile_data['role']
        profile.phone = profile_data['phone']
        profile.date_of_birth = profile_data['date_of_birth']
        if profile_data['image']:
            profile.image = profile_data['image']
        profile.speciality = profile_data['speciality']
        profile.clinic.set(profile_data['clinic'])

        instance.set_password(instance.password)
        instance.save()

        return instance


class UserProfileWithoutPasswordSerializer(WritableNestedModelSerializer):
    profile = ProfileSerializer()
    auth_token = TokenSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile', 'auth_token')


class EmployeeTokenCreateSerializer(TokenCreateSerializer):
    """
        Переопределение статус кода с HTTP_400_BAD_REQUEST на HTTP_403_FORBIDDEN
        через class ValidationError
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
                raise ValidationError('permission_denied')
        if self.user and self.user.is_active:
            return attrs
        raise ValidationError('permission_denied')
