from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from .models import DirectMessaging
from .serializers import DirectMessageSerializer


User = get_user_model()

class UserDirectMessageView(APIView):

    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
    
    def get_object(self, request, username):
        user = request.user
        other_user = self.get_user(username)
        dm = DirectMessaging.objects.get_or_create(members=[user.id,other_user.id])
        return dm

    def get(self, request, username, format=None):
        dm = self.get_object(request, username)
        serializer = DirectMessageSerializer(dm)
        return Response(serializer.data, status=status.HTTP_200_OK)