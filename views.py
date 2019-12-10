from django_kerb_auth.forms import UserForm
from django.shortcuts import render

def index(request):
    return render(request, 'base.html', {})

def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            print('VALID!')
        else:
            print('BAD')
            print(user_form._errors)
    else:
        user_form = UserForm()
    return render(request, 'forms/create_user.html', {'user_form': user_form})