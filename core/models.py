from core.call_state import BaseCallerState, CallStateChoices, choice_to_class
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from .mailing import send_email
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    username = models.CharField("Username", unique=True, max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def email_user(self, *args, **kwargs):
        send_email(
            '{}'.format(args[0]), # Subject
            '{}'.format(args[1]), # Message
            self.email,
            )


    def __str__(self):
        return self.email
       

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField("First Name", blank=True, max_length=20)
    last_name = models.CharField("Last Name", blank=True, max_length=20)
    call_state = models.CharField(max_length=10, choices=CallStateChoices.choices, default=CallStateChoices.IDLE, editable=False)
    other_caller = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, editable=False)
    
    def get_state(self) -> BaseCallerState:
       state_object =  choice_to_class[self.call_state]()
       state_object.profile = self
       return state_object


    def set_state(self, state):
        self.call_state = state
        self.save()


    def get_full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        
    def __str__(self):
        return self.user.email

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
