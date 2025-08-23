from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from accounts.serializers import UserSerializer
from role_apps.permissions import IsAdmin, IsClient, IsManager

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Base: everyone must be logged in

    def list(self, request):
        """
        Example: Any authenticated user can access
        """
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdmin])
    def admin_dashboard(self, request):
        """
        Only admin can access
        """
        return Response({"msg": "Welcome Admin!"})

    @action(detail=False, methods=['get'], permission_classes=[IsManager])
    def manager_dashboard(self, request):
        """
        Only manager can access
        """
        return Response({"msg": "Welcome Manager!"})

    @action(detail=False, methods=['get'], permission_classes=[IsClient])
    def user_dashboard(self, request):
        """
        Only normal users can access
        """
        return Response({"msg": "Welcome User!"})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def shared_page(self, request):
        """
        Any logged-in role can access
        """
        return Response({"msg": "Shared page for all roles!"})
