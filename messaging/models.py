import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class DirectMessaging(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)