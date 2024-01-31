from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Connection, CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    birthday = serializers.DateField(required=True, format='%Y-%m-%d')
    university = serializers.CharField(required=True)
    field = serializers.CharField(required=True)
    workplace = serializers.CharField(required=True, allow_blank=True)
    specialties = serializers.CharField(required=True, allow_blank=True)
    profile_photo = serializers.ImageField(required=False, max_length=None, use_url=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'birthday', 'university',
                  'field', 'workplace', 'specialties', 'profile_photo')

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            birthday=validated_data['birthday'],
            university=validated_data['university'],
            field=validated_data['field'],
            workplace=validated_data.get('workplace', None),
            specialties=validated_data.get('specialties', None),
            profile_photo=validated_data.get('profile_photo', None)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def delete(self, instance):
        instance.delete()
        

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        if not all(key in data for key in ['username', 'password']):
            raise serializers.ValidationError("Both username and password fields must be provided.")
        return data


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('id', 'user1', 'user2', 'creation_date')
        read_only_fields = ('id', 'creation_date')



    def delete(self, validated_data):
        username = validated_data.get('username')
        user2 = CustomUser.objects.get(username=username)

        connection1 = Connection.objects.filter(user1=self.context['request'].user, user2=user2)
        connection2 = Connection.objects.filter(user1=user2, user2=self.context['request'].user)

        if not (connection1.exists() or connection2.exists()):
            raise serializers.ValidationError('Connection does not exist.')

        connection1.delete()
        connection2.delete()

        return {'message': 'Connection removed successfully.'}