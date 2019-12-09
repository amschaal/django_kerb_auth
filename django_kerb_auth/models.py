from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User)

class Token(models.Model):
    TYPE_PASSWORD_RESET = 'password_reset'
    TYPE_CONFIRM_EMAIL = 'confirm_email'
    TYPE_CHOICES = ((TYPE_PASSWORD_RESET,TYPE_PASSWORD_RESET),(TYPE_CONFIRM_EMAIL,TYPE_CONFIRM_EMAIL))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(choices=TYPE_CHOICES)