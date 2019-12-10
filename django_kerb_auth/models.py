from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Token(models.Model):
    TYPE_PASSWORD_RESET = 'password_reset'
    TYPE_CONFIRM_EMAIL = 'confirm_email'
    TYPE_INVITATION = 'invitation'
    TYPE_CHOICES = ((TYPE_PASSWORD_RESET,TYPE_PASSWORD_RESET),(TYPE_CONFIRM_EMAIL,TYPE_CONFIRM_EMAIL),(TYPE_INVITATION,TYPE_INVITATION))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)