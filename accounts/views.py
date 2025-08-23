from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from accounts.serializers import LoginSerializer, RegisterSerializer


# Create your views here.

User = get_user_model

class AuthViewSet(viewsets.ViewSet):
    """
    A view set for user authentication and management
    """
    
    @action(detail=False, methods=['POST'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        response_data = serializer.create(serializer.validated_data)
        return Response(response_data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['POST'])
    def logout(self, request):
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def forgot_password(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
       
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f"http://localhost:3000/reset-password/{user.pk}/{token}/"

        send_mail(
            "Password Reset",
            f"Click the link to reset your password: {reset_link}",
            "noreply@example.com",
            [email],
        )
        return Response({"message": "Password reset link sent"})
    
    @action(detail=False, methods=["post"])
    def refresh_token(self, request):
        from rest_framework_simplejwt.views import TokenRefreshView
        view = TokenRefreshView.as_view()
        return view(request._request)
    
    
    def send_mail(self, request):
        pass