import uuid
from django.core.checks.messages import Error
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class DirectMessagingManager(models.Manager):
    def get_dm(self, people):
        dm = self.filter(first_user=people[0], second_user=people[1])
        if dm.exists():
            return dm[0]
        
        dm = self.filter(first_user=people[1], second_user=people[0])
        if dm.exists():
            return dm[0]
        
        return self.create(first_user=people[0], second_user=people[1])

    def create(self, *args, **kwargs):
        dm = self.filter(first_user=kwargs.get("second_user"), second_user=kwargs.get("first_user"))
        if dm.exists():
            return dm[0]
        return super().create(*args, **kwargs)




class DirectMessaging(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    first_user = models.ForeignKey(User, on_delete=models .CASCADE, related_name="dm_first_user")
    second_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_second_user")

    objects = DirectMessagingManager()

    def __str__(self):
        return f"{self.first_user.email} | {self.second_user.email}"
    
    class Meta:
        verbose_name = "DM"
        verbose_name_plural = "DMs"
        unique_together = [["first_user", "second_user"]]