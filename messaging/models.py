import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
class DirectMessaging(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)

    @classmethod
    def combination_exists(cls, members):
        return cls.objects.filter(members=members).exists()
        