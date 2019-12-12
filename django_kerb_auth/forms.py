from django import forms
from django.contrib.auth.models import User
from kerberos.admin import KerberosAdmin

class UserForm(forms.models.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        self.kadmin = KerberosAdmin()
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    def clean_username(self):
        username = self.cleaned_data['username']
        if self.kadmin.username_exists(username):
            raise forms.ValidationError('A user with that username already exists in the KDC.')
        return username
        