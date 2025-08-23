from rest_framework.views import APIView
from rest_framework.response import Response

from role_apps.permissions import IsAdmin

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"msg": "Hello Admin!"})
