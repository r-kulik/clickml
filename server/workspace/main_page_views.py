import random

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import django.forms as forms
from django.contrib.auth.models import User
from django.template.response import TemplateResponse

from.BasePageContext import BasePageContext


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='User', required=True, widget=forms.TextInput(attrs={'class': 'myfieldclass'}))
    first_name = forms.CharField(label='Name', required=True, widget=forms.TextInput(attrs={'class': 'myfieldclass'}))
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(attrs={'class': 'myfieldclass'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


def register(request):
    print('i got register request')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        print('i got registration form')
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=True)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            print('NEW USER WAS SAVED')
            print(new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

def register_done(request):
    return render(request, 'registration/register_done.html')


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """
    :param request: user Http reqeust to reach main page
    :return: Project main page
    """

    print('main page is rendering')
    context = BasePageContext(request)
    return TemplateResponse(request, "mainpage.html", context={'context': context})

