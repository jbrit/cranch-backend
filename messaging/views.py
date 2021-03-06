from django.http import Http404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from .models import DirectMessaging
from .serializers import DirectMessageSerializer


User = get_user_model()

class UserDirectMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    
    def get_object(self, request, username):
        user = request.user
        other_user = self.get_user(username)
        dm = DirectMessaging.objects.get_dm([user,other_user])
        return dm

    @swagger_auto_schema(responses={200: DirectMessageSerializer()})
    def get(self, request, username, format=None):
        dm = self.get_object(request, username)
        serializer = DirectMessageSerializer(dm)
        return Response(serializer.data, status=status.HTTP_200_OK)