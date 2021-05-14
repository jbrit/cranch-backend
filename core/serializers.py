from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class RegisterUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'], username=validated_data['username'])
        return user
    
    class Meta:
        model = User
        fields = ['email','username','password']