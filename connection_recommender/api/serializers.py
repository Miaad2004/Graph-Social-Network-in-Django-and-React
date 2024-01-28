from rest_framework import serializers
from .models import CustomUser, Connection
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'name', 'date_of_birth', 'university_location', 'field', 'workplace', 'specialties')
    
    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            date_of_birth = validated_data['date_of_birth'],
            university_location=validated_data['university_location'],
            field=validated_data['field'],
            workplace=validated_data['workplace'],
            specialties=validated_data['specialties']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ('id', 'user1', 'user2', 'creation_date')
        read_only_fields = ('id', 'creation_date')