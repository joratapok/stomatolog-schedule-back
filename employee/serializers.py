from rest_framework import serializers
from employee.models import Profile
from django.contrib.auth.models import User
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin


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
