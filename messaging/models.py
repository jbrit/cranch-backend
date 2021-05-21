import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()
class DirectMessaging(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    members = models.ManyToManyField(User)

    @classmethod
    def is_valid_dm(cls, members):
        # does not exist and contains two members
        return not (cls.objects.filter(members=members).exists() or len(members) != 2)
    
    def __str__(self):
        return " | ".join(list(map(lambda member: member.email, self.members.all())))
    
    class Meta:
        verbose_name = "DM"
        verbose_name_plural = "DMs"