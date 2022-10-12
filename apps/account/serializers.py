from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','last_name','email','username')

# User Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('organization', 'photo')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name','last_name','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        # check if username exists

        # confirm passwords are same


        user = User.objects.create_user(
            validated_data['username'], 
            validated_data['username'], 
            validated_data['password'],
            first_name  = validated_data['first_name'],
            last_name   = validated_data['last_name'],
            is_active   = False
            )

        return user


