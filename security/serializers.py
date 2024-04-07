from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'description',
        ]

class ProfileMeSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'permissions',
            'photo_url',
        ]


class UserMeSerializer(serializers.ModelSerializer):
    profile = ProfileMeSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'profile',
        ]


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'human_last_seen',
            'is_online',
            'email',
            'first_name',
            'last_name',
            'surname',
            'photo_url',
        ]


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'first_name',
            'last_name',
            'surname',
            'photo',
            'permissions',
            'date_of_birth',
        ]
