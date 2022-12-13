from rest_framework import serializers
from django.contrib.auth.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin
from djoser.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from djoser.serializers import TokenSerializer
from rest_framework.serializers import ModelSerializer
from djoser.serializers import TokenCreateSerializer
from employee.models import Profile


# class ProfileSerializer(UniqueFieldsMixin,  WritableNestedModelSerializer):
#     date_of_birth = serializers.DateField()
#
#     class Meta:
#         model = Profile
#         fields = ('middle_name', 'role', 'date_of_birth', 'phone', 'image', 'speciality', 'clinic')
#
#
# class UserProfileSerializer(WritableNestedModelSerializer):
#     profile = ProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'first_name', 'last_name', 'profile')
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.password = validated_data.get('password', instance.password)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#
#         profile = instance.profile
#         profile_data = validated_data.pop('profile')
#
#         profile.middle_name = profile_data['middle_name']
#         profile.role = profile_data['role']
#         profile.phone = profile_data['phone']
#         profile.date_of_birth = profile_data['date_of_birth']
#         if profile_data['image']:
#             profile.image = profile_data['image']
#         profile.speciality = profile_data['speciality']
#         profile.clinic.set(profile_data['clinic'])
#
#         instance.set_password(instance.password)
#         instance.save()
#
#         return instance


# class UserProfileWithoutPasswordSerializer(WritableNestedModelSerializer):
#     profile = ProfileSerializer()
#     auth_token = TokenSerializer()
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'profile', 'auth_token')


# class EventUserProfileSerializer(ModelSerializer):
#     profile = ProfileSerializer()
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'profile')


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


# class UserSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'is_staff')


class ProfileListSerializer(ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_of_birth = serializers.DateField()

    class Meta:
        model = Profile
        fields = (
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
        user = User.objects.create(**user_data)
        user.set_password(user_data['password'])

        clinic = validated_data.pop('clinic')
        profile = Profile.objects.create(user=user, **validated_data)
        profile.clinic.set(clinic)

        user.save()
        profile.save()
        return profile

    def update(self, instance, validated_data):
        User.objects.filter(pk=instance.user.pk).update(**validated_data.pop('user'))
        user = User.objects.get(pk=instance.user.pk)
        user.set_password(validated_data.pop('password'))
        user.save()

        super().update(instance, validated_data)

        instance.refresh_from_db()
        return instance

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     User.objects.filter(pk=instance.user.pk).update(**user_data)
    #     # instance.user.set_password(user_data['password'])
    #
    #     clinic = validated_data.pop('clinic')
    #     Profile.objects.filter(pk=instance.pk).update(**validated_data)
    #     instance.clinic.set(clinic)
    #
    #     instance.refresh_from_db()
    #     return instance


class ProfileTokenSerializer(ProfileListSerializer):
    token = serializers.CharField(source='user.auth_token.key')

    class Meta:
        model = Profile
        fields = (
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


class EventProfileSerializer(ProfileListSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.pop('password', None)
        return response
