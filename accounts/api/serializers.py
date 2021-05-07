from django.contrib.auth.models import User
from rest_framework import serializers


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active']

    def save(self, **kwargs):
        user = User(
            username=self.validated_data.get('username'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            is_active=self.validated_data.get('is_active')
        )
        user.set_password(self.validated_data.get('password'))
        user.save()
        return user

    def update(self, instance, validated_data):
        if validated_data.get('username'):
            instance.username = validated_data.get('username')
        if validated_data.get('first_name'):
            instance.first_name = validated_data.get('first_name')
        if validated_data.get('last_name'):
            instance.last_name = validated_data.get('last_name')
        if validated_data.get('is_active'):
            instance.is_active = validated_data.get('is_active')
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'is_superuser']
