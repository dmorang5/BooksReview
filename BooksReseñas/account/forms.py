from django import forms
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from .models import Profile
from django.conf import settings

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    recaptcha = ReCaptchaField(
        widget = ReCaptchaV2Checkbox(),
        error_messages = {
            'required': settings.RECAPTCHA_ERROR_MSG['required'],
        }
    )

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}))
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def clean_password2(self):
       cd = self.cleaned_data
       if cd['password'] != cd['password2']:
           raise forms.ValidationError('Passwords don\'t match.')
       return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data

class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo', 'cover_photo']