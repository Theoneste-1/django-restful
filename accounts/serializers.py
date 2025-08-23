from django.forms import fields
from rest_framework import authentication, serializers
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "date_joined"]
        
class RegisterSerializer(serializers.Serializer):
    passowrd = serializers.CharField(write_only=True, min_length=8, style={"input_type":"password"})
    class Meta:
        model = CustomUser
        fields = ["email","full_name", "passowrd"]
    
    def create(self, validate_data):
        user = CustomUser.objects.create_user(
            email = validate_data['email'],
            password = validate_data['passowrd'],
            full_name = validate_data['full_name', ""]
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta: 
        model = CustomUser
        fields = ["username", "password"]
        
    def validate(self, data):
        user = authenticate(email=[data['email']], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        if not user.is_active:
            raise serializers.ValidationError("Account is not active")
        return user
    
    def create(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            'user': UserSerializer(validated_data).data
        }