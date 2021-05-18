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

    def clean(self, *args, **kwargs):
        if len(self.members) != 2:
            raise ValidationError("Exactly two members must be present in a direct message")
        if self.combination_exists(self.members):
            raise ValidationError("This direct message already exists")