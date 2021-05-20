from rest_framework.serializers import ModelSerializer
from .models import DirectMessaging


class DirectMessageSerializer(ModelSerializer):
    class Meta:
        model = DirectMessaging
        fields = "__all__"

