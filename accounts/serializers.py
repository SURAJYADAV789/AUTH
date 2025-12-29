from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {
            'password' : {'write_only':True}
        }


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):   
        user = authenticate(
            email=data['email'],
            password = data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid Credentials")

        data['user'] = user
        return data    
