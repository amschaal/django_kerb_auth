from django import forms
from django.contrib.auth.models import User

class UserForm(forms.models.ModelForm):
    class Meta:
        model = User