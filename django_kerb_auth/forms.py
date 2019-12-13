from django import forms
from django.contrib.auth.models import User
from krbadmin.admin import KerberosAdmin
from django.db import transaction
from django.contrib.auth.forms import SetPasswordForm

class UserForm(forms.models.ModelForm, SetPasswordForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'new_password1', 'new_password2']
    def __init__(self, *args, **kwargs):
        self.kadmin = KerberosAdmin()
        super(UserForm, self).__init__(*args, **kwargs)
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
    def clean_username(self):
        username = self.cleaned_data['username']
        if self.kadmin.username_exists(username):
            raise forms.ValidationError('A user with that username already exists in the KDC.')
        return username
    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        if commit:
            with transaction.atomic():
                print('saving user')
                user = forms.models.ModelForm.save(self, commit=commit)
                print('adding principal')
                try:
                    self.kadmin.add_principal(user, password)
                    print('principal added')
                except Exception as e:
                    print('Problem with add_principal')
                    print(e.message)
                    raise e
                return user
        else:
            return forms.models.ModelForm.save(self, commit=commit)
            
class KerberosSetPasswordForm(SetPasswordForm):
    def clean(self):
        cleaned_data = super(KerberosSetPasswordForm, self).clean()
        new_password = cleaned_data.get("new_password1")
        if len(self.errors) == 0:
            try:
    #             The only way to validate a password with python kadmin is to set it.
                self.user.principal.set_password(new_password)#princ.change_password(password)
            except Exception as e:
                raise forms.ValidationError(str(e))
    def save(self, commit=True):
        #Doesn't do anything, since password setting happens in clean.
#         kadmin = KerberosAdmin.create()
#         kadmin.set_password(self.user,self.cleaned_data['new_password1'])
        return self.user
        